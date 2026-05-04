"""Command-line entry point for the WSU-GPS project."""

from pathlib import Path

from algorithms import dijkstra
from graph_data import build_graph
from map_overlay import draw_graph_on_map
from visualize import draw_graph


MAP_IMAGE = Path(__file__).parent / "data" / "wsu_pullman_map.png"
OVERLAY_OUTPUT = Path(__file__).parent / "output" / "map_overlay.png"


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
        dijkstra_path, dijkstra_cost = dijkstra(graph, start, end)
    except ValueError as error:
        print(f"Error: {error}")
        print("Please choose one of the available locations listed above.")
        return

    print_result("Dijkstra route", dijkstra_path, dijkstra_cost)

    if MAP_IMAGE.exists():
        draw_graph_on_map(
            graph,
            MAP_IMAGE,
            path=dijkstra_path,
            save_path=OVERLAY_OUTPUT,
        )
    else:
        print()
        print(f"Map image not found: {MAP_IMAGE}")
        print("Showing the plain graph layout instead.")
        print("To see the campus map overlay, save the map image at that path.")
        draw_graph(graph, dijkstra_path)


if __name__ == "__main__":
    main()
