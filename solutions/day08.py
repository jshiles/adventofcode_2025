"""Advent of Code 2025 - Day 8"""

import math
import networkx as nx
from typing import List, Tuple, Optional, Set
from dataclasses import dataclass
from itertools import combinations
from functools import lru_cache


@dataclass(frozen=True, order=True)
class Point3D:
    x: float
    y: float
    z: float

    def distance_to(self, other) -> float:
        """Calculate the Euclidean distance to another Point3D."""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)


@lru_cache
def find_pair_distances(junction_boxes: Tuple[Point3D, ...]) -> Set[Tuple[Point3D, Point3D, float]]:
    """Compute distances between all pairs of junction boxes."""
    distances = []
    for p1, p2 in combinations(sorted(junction_boxes), 2):
        distances.append((p1, p2, p1.distance_to(p2)))
    return set(distances)


def create_circuts(junction_boxes: List[Point3D], iterations: int) -> Tuple[int, Optional[Tuple[Point3D, Point3D]]]:
    """Build a graph by connecting junction boxes in order of shortest distance.

    Returns the product of sizes of the top 3 connected components and the last connected pair.
    """
    G = nx.Graph()
    G.add_nodes_from(junction_boxes)

    last_connected_points = None

    junction_boxes_distances = find_pair_distances(tuple(junction_boxes))
    connections = iterations
    for p1, p2, distance in sorted(junction_boxes_distances, key=lambda x: x[2]):
        if not nx.has_path(G, p1, p2):
            G.add_edge(p1, p2, weight=distance)
        
        connections = connections - 1
        last_connected_points = (p1, p2)

        if connections == 0 or len(list(nx.connected_components(G))) == 1:
            break

    top_3_components = sorted(nx.connected_components(G), key=len, reverse=True)[:3]
    value = 1
    for i, component in enumerate(top_3_components, 1):
        value *= len(component)

    return value, last_connected_points
    

def parse(input_text: str) -> List[Point3D]:
    """Parse the puzzle input."""
    
    junction_boxes: List[Point3D] = []

    for line in input_text.strip().split("\n"):
        if line.strip() != "":
            x, y, z = line.strip().split(",")
            junction_boxes.append(Point3D(int(x), int(y), int(z)))

    return junction_boxes


def part1(input_text: str, iterations: int = 1000) -> int:
    """Solve part 1: compute the product of sizes of the top 3 connected components."""
    junction_boxes = parse(input_text)
    val, _ = create_circuts(junction_boxes, iterations)
    return val 


def part2(input_text: str) -> int:
    """Solve part 2: find the product of x-coordinates of the last connected pair."""
    junction_boxes = parse(input_text)
    max_iterations = len(list(combinations(sorted(junction_boxes), 2)))
    _, last_connected_points = create_circuts(junction_boxes, max_iterations)
    if last_connected_points:
        return last_connected_points[0].x * last_connected_points[1].x 
    return 0


if __name__ == "__main__":
    with open("puzzle_input/day08.txt") as f:
        input_text = f.read()
    print(f"Part 1: {part1(input_text)}")
    print(f"Part 2: {part2(input_text)}")
