import networkx as nx

def build_graph():
    G = nx.Graph()

    positions = {
        "Dana": (0, 2),
        "Carpenter": (2, 2),
        "Clevland": (4, 2),
        "Todd": (6, 2),
        "CUE": (8, 2),
        "Chinook": (5, 4),
        "CUB": (7, 4),
        "Spark": (6, 0),
    }

    # Add nodes
    for node, pos in positions.items():
        G.add_node(node, pos=pos)

    # Add edges with weights
    edges = [
        ("Dana", "Carpenter", 2),
        ("Carpenter", "Clevland", 2),
        ("Clevland", "Todd", 2),
        ("Todd", "CUE", 2),

        ("Todd", "Chinook", 3),
        ("Todd", "CUB", 3),
        ("Todd", "Spark", 3),

        ("CUB", "Chinook", 2),
        ("CUB", "CUE", 2),

        # NEW EDGE
        ("Spark", "Clevland", 3),
    ]

    for u, v, w in edges:
        G.add_edge(u, v, weight=w)

    return G