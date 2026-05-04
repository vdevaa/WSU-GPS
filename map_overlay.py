"""Overlay the WSU-GPS graph on top of a campus map image.

Usage:
    python map_overlay.py data/wsu_pullman_map.png
    python map_overlay.py data/wsu_pullman_map.png --start Dana --end CUB

The location CSV coordinates should match the image coordinate system:
x is pixels from the left edge, and y is pixels from the top edge.
Use calibrate_locations.py to create those coordinates by clicking buildings.
"""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx

from algorithms import dijkstra
from graph_data import build_graph


def draw_graph_on_map(graph, map_image_path, path=None, save_path=None, show=True):
    """Draw graph nodes and edges over a campus map image."""
    image = plt.imread(map_image_path)
    height, width = image.shape[:2]
    positions = nx.get_node_attributes(graph, "pos")
    building_nodes = [node for node in graph.nodes if not node.startswith("Walkway:")]
    walkway_nodes = [node for node in graph.nodes if node.startswith("Walkway:")]
    building_labels = {node: node for node in building_nodes}

    plt.figure(figsize=(12, 9))
    plt.imshow(image, extent=(0, width, height, 0))

    nx.draw_networkx_edges(
        graph,
        positions,
        edge_color="black",
        alpha=0.35,
        width=1.5,
    )

    if path and len(path) > 1:
        highlighted_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(
            graph,
            positions,
            edgelist=highlighted_edges,
            edge_color="crimson",
            width=3,
        )

    nx.draw_networkx_nodes(
        graph,
        positions,
        nodelist=walkway_nodes,
        node_color="lightgray",
        edgecolors="black",
        node_size=45,
        linewidths=0.5,
    )
    nx.draw_networkx_nodes(
        graph,
        positions,
        nodelist=building_nodes,
        node_color="gold",
        edgecolors="black",
        node_size=160,
        linewidths=0.8,
    )
    nx.draw_networkx_labels(graph, positions, labels=building_labels, font_size=7)

    plt.title("WSU-GPS Campus Map Overlay")
    plt.xlim(0, width)
    plt.ylim(height, 0)
    plt.axis("off")
    plt.tight_layout()

    if save_path:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=200)
        print(f"Saved overlay to {save_path}")

    if show:
        plt.show()


def main():
    parser = argparse.ArgumentParser(description="Overlay WSU-GPS on a map image.")
    parser.add_argument("map_image", help="Path to a PNG or JPG campus map image")
    parser.add_argument("--start", help="Optional route start location")
    parser.add_argument("--end", help="Optional route end location")
    parser.add_argument(
        "--save",
        default="output/map_overlay.png",
        help="Output image path. Default: output/map_overlay.png",
    )
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="Save the overlay without opening a Matplotlib window",
    )
    args = parser.parse_args()

    graph = build_graph()
    route = None

    if args.start and args.end:
        route, cost = dijkstra(graph, args.start, args.end)
        print(f"Dijkstra route: {' -> '.join(route)}")
        print(f"Total cost: {cost}")

    draw_graph_on_map(
        graph,
        args.map_image,
        path=route,
        save_path=args.save,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
