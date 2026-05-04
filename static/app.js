const state = {
  graph: null,
  route: [],
  start: "Dana",
  end: "CUB",
  picking: "start",
};

const startInput = document.querySelector("#start-input");
const endInput = document.querySelector("#end-input");
const routeForm = document.querySelector("#route-form");
const swapButton = document.querySelector("#swap-button");
const routeCost = document.querySelector("#route-cost");
const routeList = document.querySelector("#route-list");
const routeError = document.querySelector("#route-error");
const mapImage = document.querySelector("#map-image");
const overlay = document.querySelector("#map-overlay");
const tooltip = document.querySelector("#map-tooltip");

function svgElement(tag, attrs = {}) {
  const element = document.createElementNS("http://www.w3.org/2000/svg", tag);
  for (const [key, value] of Object.entries(attrs)) {
    element.setAttribute(key, value);
  }
  return element;
}

function nodeById(id) {
  return state.graph.nodes.find((node) => node.id === id);
}

function routeEdgeKey(start, end) {
  return [start, end].sort().join("||");
}

function currentAlgorithm() {
  return new FormData(routeForm).get("algorithm") || "dijkstra";
}

function setEndpoint(nodeId) {
  if (state.picking === "start") {
    startInput.value = nodeId;
    state.start = nodeId;
    state.picking = "end";
  } else {
    endInput.value = nodeId;
    state.end = nodeId;
    state.picking = "start";
  }
  findRoute();
}

function showTooltip(event, node) {
  tooltip.hidden = false;
  tooltip.textContent = node.id;
  tooltip.style.left = `${event.offsetX + 12}px`;
  tooltip.style.top = `${event.offsetY + 12}px`;
}

function hideTooltip() {
  tooltip.hidden = true;
}

function renderGraph() {
  const { width, height } = state.graph.image;
  overlay.setAttribute("viewBox", `0 0 ${width} ${height}`);
  overlay.replaceChildren();

  const routeEdges = new Set();
  for (let index = 0; index < state.route.length - 1; index += 1) {
    routeEdges.add(routeEdgeKey(state.route[index], state.route[index + 1]));
  }
  const routeNodes = new Set(state.route);

  const edgeLayer = svgElement("g");
  const routeEdgeLayer = svgElement("g");
  const nodeLayer = svgElement("g");
  const labelLayer = svgElement("g");
  overlay.append(edgeLayer, routeEdgeLayer, nodeLayer, labelLayer);

  for (const edge of state.graph.edges) {
    const start = nodeById(edge.from);
    const end = nodeById(edge.to);
    const line = svgElement("line", {
      x1: start.x,
      y1: start.y,
      x2: end.x,
      y2: end.y,
      class: routeEdges.has(routeEdgeKey(edge.from, edge.to)) ? "edge route" : "edge",
    });

    if (routeEdges.has(routeEdgeKey(edge.from, edge.to))) {
      routeEdgeLayer.append(line);
    } else {
      edgeLayer.append(line);
    }
  }

  for (const node of state.graph.nodes) {
    const isSelected = node.id === startInput.value || node.id === endInput.value;
    const isRouteNode = routeNodes.has(node.id);
    const radius = node.type === "building" ? 6 : 3;
    const circle = svgElement("circle", {
      cx: node.x,
      cy: node.y,
      r: radius,
      class: `node ${node.type}${isSelected ? " selected" : ""}${isRouteNode && !isSelected ? " route-node" : ""}`,
      tabindex: node.type === "building" ? "0" : "-1",
      "aria-label": node.id,
    });

    if (node.type === "building") {
      circle.addEventListener("click", () => setEndpoint(node.id));
      circle.addEventListener("mouseenter", (event) => showTooltip(event, node));
      circle.addEventListener("mousemove", (event) => showTooltip(event, node));
      circle.addEventListener("mouseleave", hideTooltip);
      circle.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          setEndpoint(node.id);
        }
      });
    }

    nodeLayer.append(circle);
  }

  for (const nodeId of state.route) {
    const node = nodeById(nodeId);
    const label = svgElement("text", {
      x: node.x + 8,
      y: node.y - 8,
      class: "route-label",
    });
    label.textContent = node.id;
    labelLayer.append(label);
  }
}

function renderRouteSummary(payload) {
  routeError.textContent = "";
  routeCost.textContent = payload.cost == null ? "--" : `${payload.cost}`;
  routeList.replaceChildren();

  for (const stop of payload.path) {
    const item = document.createElement("li");
    item.textContent = stop;
    routeList.append(item);
  }
}

async function findRoute() {
  state.start = startInput.value.trim();
  state.end = endInput.value.trim();

  const params = new URLSearchParams({
    start: state.start,
    end: state.end,
    algorithm: currentAlgorithm(),
  });

  const response = await fetch(`/api/route?${params}`);
  const payload = await response.json();

  if (!response.ok) {
    state.route = [];
    routeError.textContent = payload.error || "Route unavailable.";
    routeCost.textContent = "--";
    routeList.replaceChildren();
    renderGraph();
    return;
  }

  state.route = payload.path;
  renderRouteSummary(payload);
  renderGraph();
}

routeForm.addEventListener("submit", (event) => {
  event.preventDefault();
  findRoute();
});

swapButton.addEventListener("click", () => {
  const currentStart = startInput.value;
  startInput.value = endInput.value;
  endInput.value = currentStart;
  findRoute();
});

startInput.addEventListener("focus", () => {
  state.picking = "start";
});

endInput.addEventListener("focus", () => {
  state.picking = "end";
});

async function boot() {
  const response = await fetch("/api/graph");
  state.graph = await response.json();
  mapImage.src = state.graph.image.url;
  await findRoute();
}

boot();
