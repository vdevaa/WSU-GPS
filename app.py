"""Flask web UI for WSU-GPS."""

from pathlib import Path
import struct

from flask import Flask, jsonify, render_template, request, send_file

from algorithms import bfs_shortest_path, dijkstra
from graph_data import build_graph


BASE_DIR = Path(__file__).parent
MAP_IMAGE = BASE_DIR / "data" / "wsu_pullman_map.png"

app = Flask(__name__)
graph = build_graph()


def read_png_size(path):
    """Return a PNG image size without adding another image dependency."""
    with open(path, "rb") as file:
        header = file.read(24)

    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"Unsupported map image format: {path}")

    width, height = struct.unpack(">II", header[16:24])
    return width, height


def public_locations():
    """Return selectable campus locations."""
    return sorted(node for node in graph.nodes if not node.startswith("Walkway:"))


def graph_payload():
    positions = dict(graph.nodes(data="pos"))
    width, height = read_png_size(MAP_IMAGE)

    nodes = [
        {
            "id": node,
            "x": position[0],
            "y": position[1],
            "type": "walkway" if node.startswith("Walkway:") else "building",
        }
        for node, position in positions.items()
    ]
    edges = [
        {"from": start, "to": end, "weight": data["weight"]}
        for start, end, data in graph.edges(data=True)
    ]

    return {
        "image": {"width": width, "height": height, "url": "/map-image"},
        "locations": public_locations(),
        "nodes": nodes,
        "edges": edges,
    }


@app.route("/")
def index():
    return render_template("index.html", locations=public_locations())


@app.route("/map-image")
def map_image():
    return send_file(MAP_IMAGE)


@app.route("/api/graph")
def api_graph():
    return jsonify(graph_payload())


@app.route("/api/route")
def api_route():
    start = request.args.get("start", "").strip()
    end = request.args.get("end", "").strip()
    algorithm = request.args.get("algorithm", "dijkstra").strip().lower()

    if algorithm == "bfs":
        route, cost = bfs_shortest_path(graph, start, end)
        algorithm_name = "BFS"
    else:
        route, cost = dijkstra(graph, start, end)
        algorithm_name = "Dijkstra"

    return jsonify(
        {
            "algorithm": algorithm_name,
            "start": start,
            "end": end,
            "path": route or [],
            "cost": cost,
        }
    )


@app.errorhandler(ValueError)
def handle_value_error(error):
    return jsonify({"error": str(error)}), 400


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
