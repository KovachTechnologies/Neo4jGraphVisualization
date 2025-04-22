# Neo4j Graph Visualizer

A web application for querying and visualizing Neo4j graph databases using a Flask backend and D3.js frontend. The application allows users to execute Cypher queries, build queries interactively through a Query Builder interface, and visualize the resulting graph with interactive nodes and relationships.

## Features

- **Interactive Graph Visualization**: Render Neo4j query results as a force-directed graph using D3.js, with draggable nodes, hover tooltips, and clickable node properties.
- **Query Builder**: Construct Cypher queries via a user-friendly interface to filter nodes by labels and properties.
- **Dynamic Styling**: Customize node colors based on labels or properties defined in a schema.
- **Responsive Design**: Adapts to different screen sizes with collapsible sidebars for query building and node details.
- **RESTful API**: Execute Cypher queries through a Flask backend with CORS support for frontend communication.

## Prerequisites

- **Python 3.8+**: Required for the Flask backend.
- **Neo4j Database**: A running Neo4j instance (local or cloud-hosted).
- **Node.js and npm** (optional): Only needed if you plan to extend the frontend with additional dependencies.
- **Web Browser**: A modern browser (e.g., Chrome, Firefox) for the frontend.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/<your-username>/neo4j-graph-visualizer.git
   cd neo4j-graph-visualizer
   ```


2. **Install Requirements**:
``` bash
pip install -r requirements.txt
```

3. **Configure credentials.json**:

Fill in with information pertinent to your neo4j instance and username and password.

``` bash
{
  "NEO4J_URI": "bolt://localhost:7687",
  "NEO4J_USERNAME": "neo4j",
  "NEO4J_PASSWORD": "your-password",
  "NEO4J_DATABASE": "neo4j"
}
```

4. **Fill in Schema.json**:

Define colors for all nodes.  Also, you can define a property and a color.  If the property condition is observed, this will supercede the definition by label.  Finally, you can set input properties for the query builder.

``` bash
{
  "default": "#D6DFEA",
  "labels": {
    "Person": "#FF6B6B",
    "Movie": "#4ECDC4"
  },
  "property": {
    "status": {
      "ACTIVE": "#2ECC71",
      "INACTIVE": "#E74C3C"
    }
  },
  "input_properties": ["name", "status"]
}
```

4. **Run the Flask Server**
``` bash
python app.py
```

## Usage
1. Access the Web Interface:
Open http://localhost:5001 in your browser.

2. Run a Cypher Query:
Enter a Cypher query in the input field (e.g., MATCH r=(n)-->(m) RETURN r LIMIT 25) and click "Run Query".

3. The graph will display nodes and relationships, with tooltips on hover and node details in the right sidebar on click.

4. Use the Query Builder:
Click the toggle button to open the Query Builder sidebar.

Select labels and properties for source and target nodes, specify a result limit, and click "Generate Query" to populate the query input.

Run the generated query to visualize the results.

5. Interact with the Graph:
Drag nodes to reposition them.

Hover over nodes to view properties in a tooltip.

Click a node to display detailed properties in the right sidebar.


## Configuration
* credentials.json: Contains Neo4j connection details (URI, username, password, database).

* schema.json:
 * default: Default node color (hex).
 * labels: Map of Neo4j labels to colors.
 * property: Map of property names and values to colors.
 * input_properties: List of properties available in the Query Builder.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
[Neo4j](https://flask.palletsprojects.com/en/stable/) for the graph database.

[D3.js](https://d3js.org/) for graph visualization.

[Flask](https://neo4j.com/) for the backend framework.
