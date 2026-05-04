"""Click building locations on a campus map to create calibrated coordinates.

Usage:
    python calibrate_locations.py data/wsu_pullman_map.png

This writes data/campus_locations_calibrated.csv by default. Review it, then
replace data/campus_locations.csv when the overlay looks correct.
"""

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt


DEFAULT_INPUT = Path(__file__).parent / "data" / "campus_locations.csv"
DEFAULT_OUTPUT = Path(__file__).parent / "data" / "campus_locations_calibrated.csv"


def read_locations(path):
    """Read location rows from a CSV file."""
    with open(path, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def write_locations(path, rows):
    """Write location rows to a CSV file."""
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "x", "y"])
        writer.writeheader()
        writer.writerows(rows)


def calibrate_locations(map_image_path, input_csv, output_csv):
    """Prompt the user to click each building on the map image."""
    calibrate_selected_locations(map_image_path, input_csv, output_csv)


def calibrate_selected_locations(map_image_path, input_csv, output_csv, only=None):
    """Prompt the user to click selected building locations on the map image."""
    rows = read_locations(input_csv)
    image = plt.imread(map_image_path)
    height, width = image.shape[:2]
    calibrated = []
    selected = set(only or [])

    if selected:
        print("Click only the selected building locations on the map.")
    else:
        print("Click each building location on the map.")
    print("Close the map window at any time to stop early.")
    print("If you skip a point, the old CSV coordinate is kept.\n")

    for row in rows:
        name = row["name"]

        if selected and name not in selected:
            calibrated.append(row)
            continue

        plt.clf()
        plt.imshow(image, extent=(0, width, height, 0))

        if calibrated:
            previous_x = [float(item["x"]) for item in calibrated]
            previous_y = [float(item["y"]) for item in calibrated]
            plt.scatter(previous_x, previous_y, c="gold", edgecolors="black", s=45)

        plt.title(f"Click location: {name}")
        plt.xlim(0, width)
        plt.ylim(height, 0)
        plt.axis("off")
        plt.draw()

        points = plt.ginput(1, timeout=0)

        if points:
            x, y = points[0]
            row["x"] = round(x, 2)
            row["y"] = round(y, 2)
            print(f"{name}: {row['x']}, {row['y']}")
        else:
            print(f"{name}: kept existing coordinate")

        calibrated.append(row)

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    write_locations(output_csv, calibrated)
    print(f"\nWrote calibrated coordinates to {output_csv}")


def main():
    parser = argparse.ArgumentParser(description="Calibrate location CSV coordinates.")
    parser.add_argument("map_image", help="Path to a PNG or JPG campus map image")
    parser.add_argument(
        "--input",
        default=DEFAULT_INPUT,
        help="Input locations CSV. Default: data/campus_locations.csv",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help="Output calibrated CSV. Default: data/campus_locations_calibrated.csv",
    )
    parser.add_argument(
        "--only",
        nargs="+",
        help="Only recalibrate these exact location names.",
    )
    args = parser.parse_args()

    calibrate_selected_locations(
        args.map_image,
        Path(args.input),
        Path(args.output),
        only=args.only,
    )


if __name__ == "__main__":
    main()
