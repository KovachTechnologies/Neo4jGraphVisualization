#!/usr/bin/env python3
"""
Flask application for querying and visualizing Neo4j graph data.

This module provides a RESTful API to execute Cypher queries against a Neo4j database,
process the results for D3.js visualization, and serve a web interface for graph exploration.
"""

import json
import logging
from typing import Dict, Any, Tuple

import neo4j
from flask import Flask, request, jsonify
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication


def load_config(file_path: str) -> Dict[str, Any]:
    """Load JSON configuration from a file."""
    with open(file_path, "r") as file:
        return json.load(file)


def connect_to_neo4j(credentials: Dict[str, str]) -> neo4j.Driver:
    """
    Establish a connection to the Neo4j database.

    Args:
        credentials: Dictionary containing Neo4j connection details
                    (URI, username, password, database name).

    Returns:
        A Neo4j driver instance.

    Raises:
        neo4j.exceptions.ServiceUnavailable: If connection to Neo4j fails.
    """
    uri = credentials["NEO4J_URI"]
    auth = (credentials["NEO4J_USERNAME"], credentials["NEO4J_PASSWORD"])
    driver = neo4j.GraphDatabase.driver(uri, auth=auth)
    driver.verify_connectivity()
    return driver


def query_database(
    credentials: Dict[str, str],
    driver: neo4j.Driver,
    query: str,
    schema: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Execute a Cypher query and process results for D3.js visualization.

    Args:
        credentials: Neo4j connection credentials.
        driver: Neo4j driver instance.
        query: Cypher query to execute.
        schema: Schema defining node colors based on properties and labels.

    Returns:
        Dictionary containing nodes and links for visualization, or an error message.
    """
    try:
        records, _, _ = driver.execute_query(query, database_=credentials["NEO4J_DATABASE"])
        nodes = {}
        links = []

        for record in records:
            rel = record["r"]
            # Process nodes
            for node in rel.nodes:
                node_id = node.element_id
                if node_id not in nodes:
                    color = schema["default"]
                    node_properties = dict(node)
                    node_labels = list(node.labels)

                    logger.debug(
                        f"Node {node_id}: properties={node_properties}, labels={node_labels}"
                    )

                    # Check properties for color assignment
                    found_property_color = False
                    for prop_name, prop_values in schema["property"].items():
                        prop_value = node_properties.get(prop_name)
                        if prop_value is not None:
                            # Case-insensitive comparison
                            prop_value_upper = str(prop_value).upper()
                            prop_values_upper = {
                                k.upper(): v for k, v in prop_values.items()
                            }
                            if prop_value_upper in prop_values_upper:
                                color = prop_values_upper[prop_value_upper]
                                found_property_color = True
                                logger.debug(
                                    f"Node {node_id}: Assigned color {color} based on "
                                    f"property {prop_name}={prop_value}"
                                )
                                break

                    # Fallback to labels if no property-based color
                    if not found_property_color:
                        for label in node_labels:
                            if label in schema["labels"]:
                                color = schema["labels"][label]
                                logger.debug(
                                    f"Node {node_id}: Assigned color {color} based on label {label}"
                                )
                                break
                        if color == schema["default"]:
                            logger.debug(
                                f"Node {node_id}: No matching label, using default color {color}"
                            )

                    nodes[node_id] = {
                        "id": node_id,
                        "labels": node_labels,
                        "properties": node_properties,
                        "color": color,
                    }

            # Process relationships
            for relationship in rel.relationships:
                links.append({
                    "source": relationship.start_node.element_id,
                    "target": relationship.end_node.element_id,
                    "type": relationship.type,
                    "properties": dict(relationship),
                })

        return {"nodes": list(nodes.values()), "links": links}
    except Exception as e:
        logger.error(f"Query execution failed: {str(e)}")
        return {"error": str(e)}


# Load configuration files
credentials = load_config("credentials.json")
schema = load_config("schema.json")
driver = connect_to_neo4j(credentials)


@app.route("/query", methods=["POST"])
def handle_query() -> Tuple[Dict[str, Any], int]:
    """
    Handle POST requests to execute Cypher queries.

    Expects a JSON payload with a 'query' field containing the Cypher query.

    Returns:
        JSON response with query results or error message, and HTTP status code.
    """
    data = request.get_json()
    query = data.get("query")
    if not query:
        return jsonify({"error": "No query provided"}), 400
    result = query_database(credentials, driver, query, schema)
    return jsonify(result), 200


@app.route("/labels", methods=["GET"])
def get_labels() -> Dict[str, Any]:
    """
    Retrieve available labels and input properties from the schema.

    Returns:
        JSON response containing lists of labels and input properties.
    """
    labels = sorted(schema["labels"].keys())
    input_properties = sorted(schema.get("input_properties", []))
    return jsonify({"labels": labels, "input_properties": input_properties})


@app.route("/")
def index() -> Any:
    """Serve the main web interface."""
    return app.send_static_file("index.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
