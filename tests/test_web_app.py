import unittest

from app import app


class WebAppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_graph_api_returns_map_and_graph_data(self):
        response = self.client.get("/api/graph")
        payload = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(payload["locations"]), 70)
        self.assertGreaterEqual(len(payload["nodes"]), 70)
        self.assertGreaterEqual(len(payload["edges"]), 100)
        self.assertEqual(payload["image"]["url"], "/map-image")

    def test_route_api_returns_dijkstra_route(self):
        response = self.client.get("/api/route?start=Dana&end=CUB")
        payload = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload["algorithm"], "Dijkstra")
        self.assertEqual(payload["cost"], 13.0)
        self.assertEqual(
            payload["path"],
            ["Dana", "Carpenter Hall", "Daggy Hall", "Murrow Center", "CUB"],
        )

    def test_route_api_reports_unknown_location(self):
        response = self.client.get(
            "/api/route?start=Not%20A%20Building&end=CUB"
        )
        payload = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("Unknown location", payload["error"])


if __name__ == "__main__":
    unittest.main()
