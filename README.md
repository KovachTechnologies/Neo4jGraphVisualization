# Neo4j Graph Visualizer

A web application for querying and visualizing Neo4j graph databases. Built with Flask (backend) and D3.js (frontend), this tool allows users to execute Cypher queries, view results as an interactive graph, and inspect node properties via hover tooltips and a collapsible sidebar. The interface is modern and aesthetically pleasing, with vibrant node colors, smooth animations, and a clean layout.

# Features
- Neo4j Integration: Connects to a Neo4j database using credentials from a JSON file.
- Cypher Query Execution: Users can input Cypher queries to retrieve graph data.
- Interactive Graph Visualization: Displays nodes and relationships using a D3.js force-directed layout.
- Node Coloring: Colors nodes based on the status property (DEGRADED = red, RESPONSIVE = green, others = cyan).
- Hover Tooltips: Shows node ID, labels, and properties when hovering over a node.
- Collapsible Sidebar: Displays detailed node properties in a right-side panel when a node is clicked.
- Modern Design: Clean typography (Inter font), vibrant colors, card-based layout, and subtle animations for a polished UI.
- Responsive Layout: Adapts to different screen sizes with a flexible container.

# Prerequisites
- Python 3.6+: Required for the Flask backend.
- Neo4j Database: A running Neo4j instance accessible via a Bolt URI.
- Node.js/Internet: For D3.js (loaded via CDN) and Google Fonts (optional, for Inter font).
- Web Browser: Chrome, Firefox, or another modern browser for optimal rendering.

# License
This project is licensed under the MIT License. See the LICENSE file for details.
