"""Manual graph algorithms for WSU-GPS.

NetworkX stores the graph, but the traversal and pathfinding logic is written
directly here for graph theory coursework.
"""

from heapq import heappop, heappush


def validate_nodes(graph, start, end):
    """Raise a helpful error if either endpoint is missing from the graph."""
    missing = [node for node in (start, end) if node not in graph]
    if missing:
        raise ValueError(f"Unknown location(s): {', '.join(missing)}")


def path_cost(graph, path):
    """Return the total edge weight for a path."""
    if not path:
        return None

    total = 0
    for index in range(len(path) - 1):
        total += graph[path[index]][path[index + 1]]["weight"]
    return total


def dijkstra(graph, start, end):
    """Find the lowest-cost path using Dijkstra's algorithm.

    Dijkstra's algorithm always expands the unvisited node with the smallest
    known distance from the start. This works well for GPS-style routing when
    all edge weights are nonnegative.
    """
    validate_nodes(graph, start, end)

    # init strcutures and priority queue
    distances = {node: float("inf") for node in graph.nodes}
    previous = {node: None for node in graph.nodes}
    distances[start] = 0

    priority_queue = [(0, start)]
    visited = set()

    while priority_queue:
        current_distance, current = heappop(priority_queue)

        if current in visited:
            continue

        visited.add(current) # have not visited yet

        if current == end:
            break # popping end node

        for neighbor in graph.neighbors(current):
            edge_weight = graph[current][neighbor]["weight"]
            new_distance = current_distance + edge_weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current
                heappush(priority_queue, (new_distance, neighbor))

    path = reconstruct_path(previous, start, end)
    return path, distances[end] if path else None


def reconstruct_path(previous, start, end):
    """Rebuild a path from a dictionary of previous-node pointers."""
    path = []
    current = end

    while current is not None:
        path.append(current)
        if current == start:
            path.reverse()
            return path
        current = previous[current]

    return None
