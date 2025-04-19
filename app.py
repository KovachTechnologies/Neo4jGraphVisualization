#!/usr/bin/python

import json
import neo4j
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for front-end communication

def connect(credentials):
    URI = credentials["NEO4J_URI"]
    AUTH = (credentials["NEO4J_USERNAME"], credentials["NEO4J_PASSWORD"])
    driver = neo4j.GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()
    return driver

def query_db(credentials, driver, query, schema):
    try:
        records, summary, keys = driver.execute_query(query, database_=credentials["NEO4J_DATABASE"])
        # Process records into nodes and relationships for D3.js
        nodes = {}
        links = []
        for record in records:
            rel = record['r']
            # Assuming 'r' is a path with nodes and relationships
            for node in rel.nodes:
                node_id = node.element_id
                if node_id not in nodes:
                    # Determine node color based on schema
                    color = schema["default"]
                    node_properties = dict(node)

                    # Log node details for debugging
                    app.logger.debug(f"Node {node_id}: properties={node_properties}, labels={list(node.labels)}")

                    # Check properties first (e.g., status, priority, etc.)
                    found_property_color = False
                    for prop_name, prop_values in schema["property"].items():
                        prop_value = node_properties.get(prop_name)
                        if prop_value is not None:
                            # Convert both the node's property value and schema keys to uppercase for case-insensitive comparison
                            prop_value_upper = str(prop_value).upper()
                            prop_values_upper = {k.upper(): v for k, v in prop_values.items()}
                            if prop_value_upper in prop_values_upper:
                                color = prop_values_upper[prop_value_upper]
                                found_property_color = True
                                app.logger.debug(f"Node {node_id}: Assigned color {color} based on property {prop_name}={prop_value}")
                                break

                    # If no property-based color, fall back to labels
                    if not found_property_color:
                        for label in node.labels:
                            if label in schema["labels"]:
                                color = schema["labels"][label]
                                app.logger.debug(f"Node {node_id}: Assigned color {color} based on label {label}")
                                break
                        if color == schema["default"]:
                            app.logger.debug(f"Node {node_id}: No matching label, using default color {color}")

                    nodes[node_id] = {
                        'id': node_id,
                        'labels': list(node.labels),
                        'properties': node_properties,
                        'color': color
                    }
            for relationship in rel.relationships:
                links.append({
                    'source': relationship.start_node.element_id,
                    'target': relationship.end_node.element_id,
                    'type': relationship.type,
                    'properties': dict(relationship)
                })
        return {'nodes': list(nodes.values()), 'links': links}
    except Exception as e:
        return {'error': str(e)}

# Load credentials and schema
with open("credentials.json", 'r') as f:
    credentials = json.load(f)
with open("schema.json", 'r') as f:
    schema = json.load(f)
driver = connect(credentials)

@app.route('/query', methods=['POST'])
def handle_query():
    data = request.get_json()
    query = data.get('query')
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    result = query_db(credentials, driver, query, schema)
    return jsonify(result)

@app.route('/labels', methods=['GET'])
def get_labels():
    labels = list(schema["labels"].keys())
    input_properties = schema.get("input_properties", [])
    return jsonify({'labels': labels, 'input_properties': input_properties})

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
