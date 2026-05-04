"""Visualization helpers for the WSU-GPS graph."""

import matplotlib.pyplot as plt
import networkx as nx


def draw_graph(graph, path=None):
    """Draw the campus graph and optionally highlight a selected route."""
    positions = nx.get_node_attributes(graph, "pos")
    edge_labels = nx.get_edge_attributes(graph, "weight")
    building_nodes = [node for node in graph.nodes if not node.startswith("Walkway:")]
    walkway_nodes = [node for node in graph.nodes if node.startswith("Walkway:")]
    building_labels = {node: node for node in building_nodes}

    plt.figure(figsize=(10, 6))

    nx.draw_networkx_edges(
        graph,
        positions,
        edge_color="lightgray",
        width=2,
    )

    if path and len(path) > 1:
        highlighted_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(
            graph,
            positions,
            edgelist=highlighted_edges,
            edge_color="crimson",
            width=4,
        )

    nx.draw_networkx_nodes(
        graph,
        positions,
        nodelist=building_nodes,
        node_color="white",
        edgecolors="black",
        node_size=1200,
        linewidths=1.5,
    )
    nx.draw_networkx_nodes(
        graph,
        positions,
        nodelist=walkway_nodes,
        node_color="lightgray",
        edgecolors="gray",
        node_size=250,
        linewidths=1,
    )
    nx.draw_networkx_labels(
        graph,
        positions,
        labels=building_labels,
        font_size=10,
        font_weight="bold",
    )
    nx.draw_networkx_edge_labels(graph, positions, edge_labels=edge_labels)

    plt.title("WSU-GPS Weighted Campus Graph")
    plt.axis("off")
    plt.tight_layout()
    plt.show()
