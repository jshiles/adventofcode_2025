"""Advent of Code 2025 - Day 12"""

import random
import re
from dataclasses import dataclass

from shapely.affinity import rotate, translate
from shapely.geometry import Polygon, box
from shapely.ops import unary_union
from shapely.strtree import STRtree


@dataclass(frozen=True)
class ShapeType:
    name: str
    geom: Polygon

    @classmethod
    def from_ascii(cls, name: str, art: str):
        return cls(name=name, geom=ascii_to_polygon(art))


@dataclass
class Puzzle:
    container: Polygon
    shape_counts: list[int]  # counts in order of shape list


def ascii_to_polygon(ascii_art: str) -> Polygon:
    """
    Converts an ASCII grid into a Shapely Polygon.
    '#' = 1x1 block
    '.' = Empty space
    """
    # 1. Clean up input strings
    lines = [line.strip() for line in ascii_art.strip().split('\n')]
    
    # 2. Determine grid dimensions
    height = len(lines)
    
    unit_boxes = []
    
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char == '#':
                y_bottom = height - 1 - r
                b = box(c, y_bottom, c + 1, y_bottom + 1)
                unit_boxes.append(b)

    if not unit_boxes:
        return Polygon()
    return unary_union(unit_boxes)


def make_container(width: int, height: int) -> box:
    return box(0, 0, width, height)


# =============================================================================
# Bin Packing Functions
# =============================================================================


def get_rotations(geom: Polygon) -> list[Polygon]:
    """Return all 4 rotations (0, 90, 180, 270 degrees) of a polygon, normalized to origin."""
    rotations = []
    for angle in [0, 90, 180, 270]:
        rotated = rotate(geom, angle, origin='centroid')
        # Normalize to origin (minx=0, miny=0)
        minx, miny, _, _ = rotated.bounds
        normalized = translate(rotated, -minx, -miny)
        rotations.append(normalized)
    return rotations


def expand_shapes(shape_types: list[ShapeType], counts: list[int]) -> list[tuple[int, Polygon]]:
    """Expand shape types by their counts into individual shapes.

    Returns list of (shape_type_idx, geometry) tuples.
    """
    shapes = []
    for idx, (shape_type, count) in enumerate(zip(shape_types, counts)):
        for _ in range(count):
            shapes.append((idx, shape_type.geom))
    return shapes


def greedy_place_count(shapes: list[Polygon], container: Polygon, step: float = 1.0) -> int:
    """Try to place shapes using greedy left-bottom placement.

    Uses STRtree for O(log N) collision detection.
    Returns the count of shapes successfully placed.
    """
    placed = []
    tree = None

    minx_c, miny_c, maxx_c, maxy_c = container.bounds

    for shape in shapes:
        shape_placed = False
        shape_minx, shape_miny, shape_maxx, shape_maxy = shape.bounds
        shape_w = shape_maxx - shape_minx
        shape_h = shape_maxy - shape_miny

        # Scan positions (bottom-left to top-right)
        y = miny_c
        while y + shape_h <= maxy_c + 1e-9 and not shape_placed:
            x = minx_c
            while x + shape_w <= maxx_c + 1e-9 and not shape_placed:
                candidate = translate(shape, x - shape_minx, y - shape_miny)

                # Check container bounds
                if not container.contains(candidate):
                    x += step
                    continue

                # Check collisions with placed shapes using STRtree
                has_collision = False
                if tree is not None:
                    collision_idxs = tree.query(candidate)
                    for i in collision_idxs:
                        if candidate.intersects(placed[i]) and not candidate.touches(placed[i]):
                            has_collision = True
                            break

                if has_collision:
                    x += step
                    continue

                # Valid placement found
                placed.append(candidate)
                tree = STRtree(placed)
                shape_placed = True

            y += step

    return len(placed)


def greedy_place(shapes: list[Polygon], container: Polygon, step: float = 1.0) -> bool:
    """Try to place all shapes using greedy left-bottom placement.

    Returns True if all shapes fit, False otherwise.
    """
    return greedy_place_count(shapes, container, step) == len(shapes)


def crossover(parent1: tuple, parent2: tuple) -> tuple:
    """Order crossover (OX) for permutation + uniform crossover for rotations."""
    order1, rot1 = parent1
    order2, rot2 = parent2
    n = len(order1)

    if n < 2:
        return (order1[:], rot1[:])

    # OX crossover for order
    start, end = sorted(random.sample(range(n), 2))
    child_order = [-1] * n
    child_order[start:end] = order1[start:end]

    segment_set = set(order1[start:end])
    remaining = [x for x in order2 if x not in segment_set]
    j = 0
    for i in range(n):
        if child_order[i] == -1:
            child_order[i] = remaining[j]
            j += 1

    # Uniform crossover for rotations
    child_rot = [rot1[i] if random.random() < 0.5 else rot2[i] for i in range(n)]

    return (child_order, child_rot)


def mutate(gene: tuple, rate: float) -> tuple:
    """Swap mutation for order, random reset for rotations."""
    order, rotations = gene
    order = order[:]
    rotations = rotations[:]

    # Swap two positions in order
    if len(order) >= 2 and random.random() < rate:
        i, j = random.sample(range(len(order)), 2)
        order[i], order[j] = order[j], order[i]

    # Mutate rotations
    for i in range(len(rotations)):
        if random.random() < rate:
            rotations[i] = random.randint(0, 3)

    return (order, rotations)


def solve_with_ga(
    shape_types: list[ShapeType],
    puzzle: Puzzle,
    population_size: int = 50,
    generations: int = 100,
    mutation_rate: float = 0.1,
) -> bool:
    """Use genetic algorithm to find a valid placement order.

    Gene = (order permutation, rotation indices) representing placement order and rotation.
    Fitness = number of shapes successfully placed by greedy algorithm.
    """
    # Pre-compute all rotations for each shape type
    all_rotations = [get_rotations(st.geom) for st in shape_types]

    # Expand shapes by count
    expanded = expand_shapes(shape_types, puzzle.shape_counts)
    total_shapes = len(expanded)

    if total_shapes == 0:
        return True

    def random_gene():
        order = list(range(total_shapes))
        random.shuffle(order)
        rotations = [random.randint(0, 3) for _ in range(total_shapes)]
        return (order, rotations)

    def fitness(gene):
        order, rotations = gene
        shapes_to_place = []
        for i in order:
            type_idx, _ = expanded[i]
            rot_idx = rotations[i]
            shapes_to_place.append(all_rotations[type_idx][rot_idx])
        return greedy_place_count(shapes_to_place, puzzle.container)

    # Initialize population
    population = [random_gene() for _ in range(population_size)]

    for _ in range(generations):
        # Evaluate fitness
        scored = [(fitness(g), g) for g in population]
        scored.sort(reverse=True, key=lambda x: x[0])

        # Check for solution
        if scored[0][0] == total_shapes:
            return True

        # Selection: keep top 50%
        survivors = [g for _, g in scored[: population_size // 2]]

        # Ensure we have at least 2 survivors for crossover
        if len(survivors) < 2:
            survivors = [g for _, g in scored]

        # Crossover and mutation to refill population
        new_population = survivors[:]
        while len(new_population) < population_size:
            p1, p2 = random.sample(survivors, 2)
            child = crossover(p1, p2)
            child = mutate(child, mutation_rate)
            new_population.append(child)

        population = new_population

    # Final check
    scored = [(fitness(g), g) for g in population]
    return max(s[0] for s in scored) == total_shapes


def can_fit(shape_types: list[ShapeType], puzzle: Puzzle) -> bool:
    """Determine if all shapes can fit in the puzzle's container."""
    return solve_with_ga(shape_types, puzzle)


def parse(input_text: str) -> tuple[list[ShapeType], list[Puzzle]]:
    """Parse the puzzle input.

    Returns:
        tuple of (list of ShapeTypes, list of Puzzles)
    """
    lines = input_text.strip().split('\n')

    # Parse shapes section (format: "name:" followed by ASCII art lines)
    shapes = []
    shape_pattern = re.compile(r'^(\d+):$')
    puzzle_pattern = re.compile(r'^(\d+)x(\d+):\s*(.+)$')

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Check if this is a shape definition
        shape_match = shape_pattern.match(line)
        if shape_match:
            name = shape_match.group(1)
            # Collect the ASCII art lines until we hit a blank line or another definition
            art_lines = []
            i += 1
            while i < len(lines):
                art_line = lines[i]
                # Stop if blank line or new definition
                if not art_line.strip() or shape_pattern.match(art_line.strip()) or puzzle_pattern.match(art_line.strip()):
                    break
                art_lines.append(art_line)
                i += 1

            if art_lines:
                art = '\n'.join(art_lines)
                shapes.append(ShapeType.from_ascii(name, art))
            continue

        # Check if this is a puzzle definition
        puzzle_match = puzzle_pattern.match(line)
        if puzzle_match:
            break  # Start of puzzles section

        i += 1

    # Parse puzzles section (format: "WxH: n1 n2 n3 n4 n5 n6")
    puzzles = []
    while i < len(lines):
        line = lines[i].strip()
        puzzle_match = puzzle_pattern.match(line)
        if puzzle_match:
            width = int(puzzle_match.group(1))
            height = int(puzzle_match.group(2))
            counts_str = puzzle_match.group(3)
            counts = [int(x) for x in counts_str.split()]

            container = make_container(width, height)
            puzzles.append(Puzzle(container=container, shape_counts=counts))
        i += 1

    return shapes, puzzles


def part1(input_text: str) -> int:
    """Solve part 1."""
    shapes, puzzles = parse(input_text)
    return sum([1 for puzzle in puzzles if can_fit(shapes, puzzle)])


def part2(input_text: str) -> int:
    """Solve part 2."""
    shapes, puzzles = parse(input_text)
    return 0


if __name__ == "__main__":
    with open("puzzle_input/day12.txt") as f:
        input_text = f.read()
    print(f"Part 1: {part1(input_text)}")
    print(f"Part 2: {part2(input_text)}")
