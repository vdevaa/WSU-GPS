# WSU-GPS

WSU-GPS is a graph theory final project that models Washington State University Pullman as a weighted graph. Campus buildings and landmarks are vertices, and direct walking paths are weighted edges.

The main demo is a Flask web app that lets a user choose two campus locations, run Dijkstra's algorithm, and view the selected path on a WSU map.

## Demo

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the web app:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

Suggested demo route:

```text
Dana -> CUB
```

Expected Dijkstra route:

```text
Dana -> Carpenter Hall -> Daggy Hall -> Murrow Center -> CUB
Total cost: 13.0
```

Current graph size:

- 74 locations
- 131 walking connections


## Tests

Run all tests:

```bash
python -m unittest discover -s tests -v
```