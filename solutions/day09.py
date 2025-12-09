"""Advent of Code 2025 - Day 9"""

import networkx as nx
from dataclasses import dataclass
from itertools import combinations, pairwise
from shapely import geometry 
from typing import List


@dataclass(frozen=True)
class Point:
    """A 2D point with integer coordinates."""
    x: int
    y: int

    def area(self, other: "Point") -> int:
        """Calculate the area of the rectangle formed by this point and another.

        Args:
            other: The opposite corner of the rectangle.

        Returns:
            The area of the axis-aligned rectangle, inclusive of boundary points.
        """
        return (abs(self.x - other.x) +1) * (abs(self.y - other.y) +1)


def largest_rectangle(points: List[Point]) -> int:
    """Find the largest axis-aligned rectangle formed by any two points.

    Args:
        points: List of points to consider as rectangle corners.

    Returns:
        The maximum area of any rectangle formed by two points.
    """
    max_rect_area = 0
    for p1, p2 in combinations(points, 2):
        max_rect_area = max(p1.area(p2), max_rect_area)

    return max_rect_area


def find_polygons(points: List[Point]) -> List[geometry.Polygon]:
    """Find all polygons formed by cycles in a graph of connected points.

    Creates a graph where consecutive points are connected, then extracts
    all cycle bases as Shapely polygons.

    Args:
        points: List of points representing vertices in order.

    Returns:
        List of Shapely Polygon objects representing closed cycles.
    """
    G = nx.Graph()

    for p in points:
        G.add_node(p, pos=(p.x, p.y))

    G.add_edges_from([(p1, p2) for p1, p2 in pairwise(points + points[:1])])

    polygons: List[geometry.Polygon] = []
    for cycle in nx.cycle_basis(G):
        coords = [G.nodes[n]['pos'] for n in cycle]
        polygon = geometry.Polygon(coords)
        polygons.append(polygon)

    return polygons


def largest_rectangle_in_polygon(polygon: geometry.Polygon, points: List[Point]) -> int:
    """Find the largest axis-aligned rectangle fully contained within a polygon.

    Tests all pairs of points as potential rectangle corners and returns
    the maximum area of rectangles that are completely covered by the polygon.

    Args:
        polygon: The bounding polygon that must fully contain the rectangle.
        points: List of candidate points for rectangle corners.

    Returns:
        The maximum area of any valid rectangle, or 0 if none exist.
    """
    max_rect_area = 0
    for p1, p2 in combinations(points, 2):
        rectangle = geometry.box(p1.x, p1.y, p2.x, p2.y)
        if polygon.covers(rectangle):
            max_rect_area = max(p1.area(p2), max_rect_area)

    return max_rect_area


def parse(input_text: str) -> List[Point]:
    """Parse the puzzle input into a list of points.

    Args:
        input_text: Raw puzzle input with one "x,y" coordinate pair per line.

    Returns:
        List of Point objects parsed from the input.
    """
    points: List[Point] = []
    for line in input_text.strip().splitlines():
        x, y = line.split(",")
        points.append(Point(int(x), int(y)))

    return points


def part1(input_text: str) -> int:
    """Solve part 1: Find the largest rectangle from any two points.

    Args:
        input_text: Raw puzzle input.

    Returns:
        The maximum rectangle area.
    """
    points = parse(input_text)
    return largest_rectangle(points)


def part2(input_text: str) -> int:
    """Solve part 2: Find the largest rectangle contained within any polygon.

    Args:
        input_text: Raw puzzle input.

    Returns:
        The maximum rectangle area contained within a polygon.
    """
    points = parse(input_text)
    polygons = find_polygons(points)
    return max([largest_rectangle_in_polygon(p, points) for p in polygons])


if __name__ == "__main__":
    with open("puzzle_input/day09.txt") as f:
        input_text = f.read()
    print(f"Part 1: {part1(input_text)}")
    print(f"Part 2: {part2(input_text)}")
