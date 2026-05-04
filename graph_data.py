"""Graph data loading for the WSU-GPS campus model."""

import csv
from pathlib import Path

import networkx as nx


DATA_DIR = Path(__file__).parent / "data"
LOCATIONS_FILE = DATA_DIR / "campus_locations.csv"
EDGES_FILE = DATA_DIR / "campus_edges.csv"


def build_graph(
    locations_file=LOCATIONS_FILE,
    edges_file=EDGES_FILE,
):
    """Create and return an undirected weighted graph from CSV files."""
    graph = nx.Graph()

    load_locations(graph, locations_file)
    load_edges(graph, edges_file)

    return graph


def load_locations(graph, locations_file):
    """Add location nodes from a CSV file with name,x,y columns."""
    with open(locations_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            name = row["name"].strip()
            x = float(row["x"])
            y = float(row["y"])
            graph.add_node(name, pos=(x, y))


def load_edges(graph, edges_file):
    """Add weighted walking edges from a CSV file with from,to,weight columns."""
    with open(edges_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            start = row["from"].strip()
            end = row["to"].strip()
            weight = float(row["weight"])

            if start not in graph or end not in graph:
                raise ValueError(f"Edge references unknown location: {start} -> {end}")

            graph.add_edge(start, end, weight=weight)
