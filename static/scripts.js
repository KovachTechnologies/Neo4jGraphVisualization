let width = 800, height = 600;

// Set up SVG canvas
const svg = d3.select("#graph")
    .append("svg")
    .attr("height", height);

// Set up tooltip and sidebars
const tooltip = d3.select("#tooltip");
const leftSidebar = d3.select("#left-sidebar");
const sidebar = d3.select("#sidebar");
const nodeProperties = d3.select("#node-properties");

// Set up force simulation
const simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(d => d.id).distance(100))
    .force("charge", d3.forceManyBody().strength(-200))
    .force("center", d3.forceCenter(width / 2, height / 2));

// Update SVG width dynamically
function updateSvgWidth() {
    const mainContent = document.querySelector(".main-content");
    width = mainContent.offsetWidth;
    svg.attr("width", width);
    simulation.force("center", d3.forceCenter(width / 2, height / 2));
    simulation.alpha(1).restart();
}

// Fetch labels and properties, then populate Query Builder
async function loadLabelsAndProperties() {
    try {
        const response = await fetch('/labels');
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();

        // Render labels
        const labels = data.labels.sort().reverse(); // Sort descending
        const labelList = d3.select("#label-list");
        labels.forEach(label => {
            const row = labelList.append("div")
                .attr("class", "label-row")
                .attr("data-label", label);

            row.append("span")
                .attr("class", "label-name")
                .text(label);

            const checkboxGroup = row.append("div")
                .attr("class", "checkbox-group");

            // Source checkbox
            checkboxGroup.append("input")
                .attr("type", "checkbox")
                .attr("id", `source-label-${label}`)
                .attr("data-type", "source")
                .on("change", updateLabelCheckboxes);
            checkboxGroup.append("label")
                .attr("for", `source-label-${label}`)
                .text("Source");

            // Target checkbox
            checkboxGroup.append("input")
                .attr("type", "checkbox")
                .attr("id", `target-label-${label}`)
                .attr("data-type", "target")
                .on("change", updateLabelCheckboxes);
            checkboxGroup.append("label")
                .attr("for", `target-label-${label}`)
                .text("Target");

            // Both checkbox
            checkboxGroup.append("input")
                .attr("type", "checkbox")
                .attr("id", `both-label-${label}`)
                .attr("data-type", "both")
                .on("change", updateLabelCheckboxes);
            checkboxGroup.append("label")
                .attr("for", `both-label-${label}`)
                .text("Both");
        });

        // Render properties
        const properties = data.input_properties.sort().reverse(); // Sort descending
        const propertyList = d3.select("#property-list");
        properties.forEach(property => {
            const row = propertyList.append("div")
                .attr("class", "property-row")
                .attr("data-property", property);

            row.append("span")
                .attr("class", "property-name")
                .text(property);

            const checkboxGroup = row.append("div")
                .attr("class", "checkbox-group");

            // Source checkbox
            checkboxGroup.append("input")
                .attr("type", "checkbox")
                .attr("id", `source-property-${property}`)
                .attr("data-type", "source")
                .on("change", updatePropertyCheckboxes);
            checkboxGroup.append("label")
                .attr("for", `source-property-${property}`)
                .text("Source");

            // Target checkbox
            checkboxGroup.append("input")
                .attr("type", "checkbox")
                .attr("id", `target-property-${property}`)
                .attr("data-type", "target")
                .on("change", updatePropertyCheckboxes);
            checkboxGroup.append("label")
                .attr("for", `target-property-${property}`)
                .text("Target");

            // Both checkbox
            checkboxGroup.append("input")
                .attr("type", "checkbox")
                .attr("id", `both-property-${property}`)
                .attr("data-type", "both")
                .on("change", updatePropertyCheckboxes);
            checkboxGroup.append("label")
                .attr("for", `both-property-${property}`)
                .text("Both");

            // Input field
            row.append("input")
                .attr("type", "text")
                .attr("class", "property-input")
                .attr("id", `input-${property}`)
                .attr("placeholder", "Value");
        });
    } catch (error) {
        console.error("Failed to load labels and properties:", error);
        alert("Failed to load labels and properties. Please check the server and try again.");
    }
}

// Ensure "Both" overrides Source/Target for labels
function updateLabelCheckboxes(event) {
    const checkbox = event.target;
    const label = checkbox.closest(".label-row").dataset.label;
    const type = checkbox.dataset.type;
    const sourceCheckbox = document.getElementById(`source-label-${label}`);
    const targetCheckbox = document.getElementById(`target-label-${label}`);
    const bothCheckbox = document.getElementById(`both-label-${label}`);

    if (type === "both" && checkbox.checked) {
        sourceCheckbox.checked = false;
        targetCheckbox.checked = false;
    } else if ((type === "source" || type === "target") && checkbox.checked) {
        bothCheckbox.checked = false;
    }
}

// Ensure "Both" overrides Source/Target for properties
function updatePropertyCheckboxes(event) {
    const checkbox = event.target;
    const property = checkbox.closest(".property-row").dataset.property;
    const type = checkbox.dataset.type;
    const sourceCheckbox = document.getElementById(`source-property-${property}`);
    const targetCheckbox = document.getElementById(`target-property-${property}`);
    const bothCheckbox = document.getElementById(`both-property-${property}`);

    if (type === "both" && checkbox.checked) {
        sourceCheckbox.checked = false;
        targetCheckbox.checked = false;
    } else if ((type === "source" || type === "target") && checkbox.checked) {
        bothCheckbox.checked = false;
    }
}

// Generate Cypher query
function generateQuery() {
    // Handle labels
    const labelRows = document.querySelectorAll(".label-row");
    const sourceLabels = [];
    const targetLabels = [];
    const bothLabels = [];

    labelRows.forEach(row => {
        const label = row.dataset.label;
        const sourceChecked = row.querySelector(`#source-label-${label}`).checked;
        const targetChecked = row.querySelector(`#target-label-${label}`).checked;
        const bothChecked = row.querySelector(`#both-label-${label}`).checked;

        if (bothChecked) {
            bothLabels.push(label);
        } else {
            if (sourceChecked) sourceLabels.push(label);
            if (targetChecked) targetLabels.push(label);
        }
    });

    const finalSourceLabels = [...bothLabels, ...sourceLabels];
    const finalTargetLabels = [...bothLabels, ...targetLabels];
    const sourceLabelStr = finalSourceLabels.length ? `:${finalSourceLabels.join(":")}` : "";
    const targetLabelStr = finalTargetLabels.length ? `:${finalTargetLabels.join(":")}` : "";

    // Handle properties
    const propertyRows = document.querySelectorAll(".property-row");
    const sourceProperties = {};
    const targetProperties = {};

    propertyRows.forEach(row => {
        const property = row.dataset.property;
        const sourceChecked = row.querySelector(`#source-property-${property}`).checked;
        const targetChecked = row.querySelector(`#target-property-${property}`).checked;
        const bothChecked = row.querySelector(`#both-property-${property}`).checked;
        const value = row.querySelector(`#input-${property}`).value.trim();

        if (value) { // Only include if a value is provided
            if (bothChecked) {
                sourceProperties[property] = value;
                targetProperties[property] = value;
            } else {
                if (sourceChecked) sourceProperties[property] = value;
                if (targetChecked) targetProperties[property] = value;
            }
        }
    });

    // Build property strings
    const sourcePropsStr = Object.keys(sourceProperties).length
        ? ` {${Object.entries(sourceProperties).map(([key, val]) => `${key}: "${val}"`).join(", ")}}`
        : "";
    const targetPropsStr = Object.keys(targetProperties).length
        ? ` {${Object.entries(targetProperties).map(([key, val]) => `${key}: "${val}"`).join(", ")}}`
        : "";

    const limit = document.getElementById("limit-input").value || 25;
    const query = `MATCH r=(n${sourceLabelStr}${sourcePropsStr})-->(m${targetLabelStr}${targetPropsStr}) RETURN r LIMIT ${limit}`;
    document.getElementById("query-input").value = query;
}

// Handle sidebar buttons
d3.select("#close-sidebar").on("click", () => {
    sidebar.classed("collapsed", true);
});

d3.select("#close-left-sidebar").on("click", () => {
    leftSidebar.classed("collapsed", true);
});

d3.select("#toggle-left-sidebar").on("click", (event) => {
    event.preventDefault();
    const isCollapsed = leftSidebar.classed("collapsed");
    leftSidebar.classed("collapsed", !isCollapsed);
});

// Handle Query Builder form submission
document.getElementById("query-builder-form").addEventListener("submit", (e) => {
    e.preventDefault();
    generateQuery();
});

// Handle window resize
window.addEventListener("resize", updateSvgWidth);

// Drag functions
function dragstarted(event, d) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}

function dragged(event, d) {
    d.fx = event.x;
    d.fy = d.y;
}

function dragended(event, d) {
    if (!event.active) simulation.alphaTarget(0);
}

// Normalize hex color to ensure consistency
function normalizeHexColor(color) {
    if (!color || !color.startsWith('#')) {
        return '#D6DFEA'; // Fallback to default if invalid
    }
    // Ensure 6 digits (some hex colors might be shorthand, e.g., #FFF)
    if (color.length === 4) {
        color = `#${color[1]}${color[1]}${color[2]}${color[2]}${color[3]}${color[3]}`;
    }
    return color.toLowerCase();
}

// Handle form submission
document.getElementById("query-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const query = document.getElementById("query-input").value;

    // Send query to server
    const response = await fetch('/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
    });
    const data = await response.json();

    if (data.error) {
        alert("Error: " + data.error);
        return;
    }

    // Clear previous graph
    svg.selectAll("*").remove();
    sidebar.classed("collapsed", true);
    leftSidebar.classed("collapsed", true);

    // Draw graph
    const links = svg.append("g")
        .selectAll("line")
        .data(data.links)
        .enter().append("line")
        .attr("class", "link");

    const nodes = svg.append("g")
        .selectAll("g")
        .data(data.nodes)
        .enter().append("g")
        .attr("class", "node")
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));

    nodes.append("circle")
        .attr("r", 5)
        .attr("fill", d => normalizeHexColor(d.color))
        .on("mouseover", function(event, d) {
            const props = Object.entries(d.properties)
                .map(([key, value]) => `${key}: ${value}`)
                .join("\n");
            tooltip
                .style("opacity", 1)
                .html(`ID: ${d.id}\nLabels: ${d.labels.join(", ")}\n${props}`)
                .style("left", (event.pageX + 10) + "px")
                .style("top", (event.pageY - 10) + "px");
        })
        .on("mouseout", function() {
            tooltip.style("opacity", 0);
        })
        .on("click", function(event, d) {
            const props = Object.entries(d.properties)
                .map(([key, value]) => `<li><strong>${key}:</strong> ${value}</li>`)
                .join("");
            nodeProperties.html(`
                <li><strong>ID:</strong> ${d.id}</li>
                <li><strong>Labels:</strong> ${d.labels.join(", ")}</li>
                ${props}
            `);
            sidebar.classed("collapsed", false);
        });

    nodes.append("text")
        .attr("dx", 12)
        .attr("dy", ".35em")
        .text(d => d.properties.name || d.id.split(':').pop());

    // Update simulation
    simulation.nodes(data.nodes)
        .on("tick", () => {
            links
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);
            nodes
                .attr("transform", d => `translate(${d.x},${d.y})`);
        });

    simulation.force("link").links(data.links);
    updateSvgWidth();
    simulation.alpha(1).restart();
});

// Initial setup
updateSvgWidth();
loadLabelsAndProperties();
