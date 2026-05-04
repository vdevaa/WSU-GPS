import unittest

from algorithms import dijkstra, path_cost
from graph_data import build_graph


class RouteTimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = build_graph()

    def test_all_route_times_are_positive(self):
        for start, end, data in self.graph.edges(data=True):
            with self.subTest(start=start, end=end):
                self.assertGreater(data["weight"], 0)

    def test_dijkstra_returns_expected_route_times(self):
        cases = [
            (
                "Dana",
                "CUB",
                ["Dana", "Carpenter Hall", "Daggy Hall", "Murrow Center", "CUB"],
                13.0,
            ),
            (
                "Student Recreation Center",
                "CUB",
                [
                    "Student Recreation Center",
                    "Beasley Coliseum",
                    "GESA Field at Martin Stadium",
                    "Information Technology Building",
                    "The CUE",
                    "CUB",
                ],
                19.0,
            ),
            (
                "Northside Residence Hall",
                "CUB",
                [
                    "Northside Residence Hall",
                    "Chinook Student Center",
                    "Avery Hall",
                    "Bryan Hall",
                    "Terrell Library",
                    "CUB",
                ],
                15.0,
            ),
            (
                "Veterinary Teaching Hospital",
                "CUB",
                ["Veterinary Teaching Hospital", "Bustad Hall", "The CUE", "CUB"],
                7.0,
            ),
            (
                "Food Service Building",
                "CUB",
                [
                    "Food Service Building",
                    "Grimes Way Playfield",
                    "Fine Arts Center",
                    "Information Technology Building",
                    "The CUE",
                    "CUB",
                ],
                23.0,
            ),
        ]

        for start, end, expected_path, expected_time in cases:
            with self.subTest(start=start, end=end):
                path, time = dijkstra(self.graph, start, end)

                self.assertEqual(path, expected_path)
                self.assertEqual(time, expected_time)
                self.assertEqual(path_cost(self.graph, path), expected_time)

    def test_unknown_location_raises_clear_error(self):
        with self.assertRaisesRegex(ValueError, "Unknown location"):
            dijkstra(self.graph, "Not A Real Building", "CUB")


if __name__ == "__main__":
    unittest.main()
