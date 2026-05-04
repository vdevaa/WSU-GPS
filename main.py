"""Command-line entry point for the Phase 1 WSU-GPS project."""

from algorithms import bfs_shortest_path, dijkstra
from graph_data import build_graph
from visualize import draw_graph


def choose_location(prompt, default):
    """Ask the user for a location, using a default when they press Enter."""
    answer = input(f"{prompt} [{default}]: ").strip()
    return answer if answer else default


def print_result(name, path, cost):
    """Print an algorithm result in a readable format."""
    if path is None:
        print(f"{name}: no route found")
        return

    print(f"{name}: {' -> '.join(path)}")
    print(f"Total cost: {cost}")


def main():
    graph = build_graph()
    locations = [node for node in graph.nodes if not node.startswith("Walkway:")]

    print("WSU-GPS Phase 2")
    print("Available locations:", ", ".join(sorted(locations)))
    print("Press Enter to use the default example route.\n")

    start = choose_location("Start location", "Dana")
    end = choose_location("Destination", "CUB")
    print()

    try:
        bfs_path, bfs_cost = bfs_shortest_path(graph, start, end)
        dijkstra_path, dijkstra_cost = dijkstra(graph, start, end)
    except ValueError as error:
        print(f"Error: {error}")
        print("Please choose one of the available locations listed above.")
        return

    print_result("BFS fewest-segments route", bfs_path, bfs_cost)
    print()
    print_result("Dijkstra weighted shortest route", dijkstra_path, dijkstra_cost)

    draw_graph(graph, dijkstra_path)


if __name__ == "__main__":
    main()
