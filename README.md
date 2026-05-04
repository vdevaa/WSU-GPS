# WSU-GPS

WSU-GPS is a graph theory final project that models part of Washington State University Pullman as a weighted graph. Campus buildings and locations are vertices, and direct walking paths are edges.

The current version is Phase 2: an expanded CSV-backed graph with major WSU Pullman academic and campus buildings.

## Graph Model

The graph is an undirected weighted graph built with NetworkX and loaded from CSV files.

- Nodes represent campus buildings or locations.
- Each node stores an `(x, y)` coordinate for drawing the graph.
- Edges represent direct walking paths.
- Edge weights represent approximate walking cost. Later versions can replace these with more realistic walking time, distance, or difficulty.

Data files:

- `data/campus_locations.csv` stores location names and approximate grid coordinates.
- `data/campus_edges.csv` stores direct walking connections and edge weights.

The current graph includes 78 building and campus landmark locations, including:

- Abelson Hall
- Avery Hall
- Bryan Hall
- Bustad Hall
- Carpenter Hall
- Cleveland Hall
- CUB
- Dana
- Daggy Hall
- Electrical-Mechanical Engineering Building
- Fine Arts Center
- Fulmer Complex
- Terrell Library
- The CUE
- The Spark
- Todd Hall
- Beasley Coliseum
- Bailey-Brayton Field
- GESA Field at Martin Stadium
- Mooberry Track
- Veterinary Teaching Hospital
- Food Service Building
- Student Recreation Center
- Northside Residence Hall
- Gannon-Goldsworthy Hall
- Stephenson Complex
- Southside Cafe

## Algorithms

### Breadth-First Search

BFS is used as a baseline unweighted shortest path algorithm. It finds the route with the fewest path segments, but it ignores walking cost.

### Dijkstra's Algorithm

Dijkstra's algorithm is the main weighted shortest path algorithm. It chooses routes using edge weights, so it is better than BFS for GPS-style routing where some paths are longer, slower, steeper, or more difficult than others.

## How To Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
python main.py
```

The program lists available locations and asks for a start and destination. Press Enter twice to use the default example route from `Dana` to `CUB`.

## Verifying The Map

The current coordinates are approximate. To verify and correct them, save an official WSU Pullman map image as:

```text
data/wsu_pullman_map.png
```

Good official references:

- WSU Maps: <https://maps.wsu.edu/>
- Pullman campus core map PDF: <https://pullman.wsu.edu/classrooms/documents/2024/05/pullman-campus-core.pdf>

Then click each building location to create calibrated coordinates:

```bash
python calibrate_locations.py data/wsu_pullman_map.png
```

This creates:

```text
data/campus_locations_calibrated.csv
```

After reviewing it, replace `data/campus_locations.csv` with the calibrated file.

To draw the graph over the map:

```bash
python map_overlay.py data/wsu_pullman_map.png --start Dana --end CUB
```

The overlay is saved to:

```text
output/map_overlay.png
```

## Example Route

For the default route from `Dana` to `CUB`:

- BFS may return the route with the fewest segments.
- Dijkstra returns the route with the lowest total walking cost.

Example weighted route:

```text
Dana -> Carpenter Hall -> Daggy Hall -> Murrow Center -> CUB
Total cost: 4.0
```

## Why Dijkstra Is Better Than BFS For GPS Routing

BFS only counts how many edges are in a path. That is useful for an unweighted graph, but it does not know whether one walking segment is short and flat or long and difficult.

Dijkstra's algorithm uses edge weights. This makes it a better model for real walking directions because the app can prefer lower-cost routes instead of simply choosing the route with the fewest turns or segments.

## Next Development Phases

1. Review and refine the expanded building list.
2. Add more residence halls, dining centers, athletics buildings, and campus landmarks.
3. Improve edge weights using approximate walking distance or walking time.
4. Replace placeholder weights with walking-time estimates from Google Maps.
5. Possibly overlay the graph on a campus map image.

When expanding the graph, use WSU's official Pullman campus map and official building or classroom lists as references for layout and building names.
