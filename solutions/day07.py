"""Advent of Code 2025 - Day 5"""

from typing import List
from functools import lru_cache


def num_splits_quantum(manifold: List[List[str]]) -> int:
    """Count total splits using memoized recursion to handle quantum superposition.

    Uses a recursive approach with caching to count the number of times a beam
    hits a '^' splitter. Each split creates two beams that can independently
    continue through the manifold.

    Args:
        manifold: 2D grid where 'S' marks the start, '^' marks splitters.

    Returns:
        Total number of split events across all possible beam paths.
    """

    @lru_cache(maxsize=None)
    def _recursive_manifold(manifold: tuple[tuple[str, ...], ...], tachyon_idx: int) -> int:

        if not (0 <= tachyon_idx < len(manifold[0])):
            return 0

        if len(manifold) == 1:
            return 1

        if manifold[0][tachyon_idx] == '^':
            return _recursive_manifold(manifold[1:], tachyon_idx - 1) + _recursive_manifold(manifold[1:], tachyon_idx + 1)

        return _recursive_manifold(manifold[1:], tachyon_idx)

    # Convert to tuple of tuples for hashability
    manifold_tuple = tuple(tuple(row) for row in manifold)
    tachyon_idx_start = min([idx for idx, x in enumerate(manifold_tuple[0]) if x == 'S'])
    return _recursive_manifold(manifold_tuple[1:], tachyon_idx_start)


def num_splits(manifold) -> int:
    """Count total splits as beams traverse the manifold, merging at same positions.

    Simulates beam propagation row by row. Beams at the same position merge into one.
    When a beam hits a '^' splitter, it counts as a hit and the beam splits left/right.

    Args:
        manifold: 2D grid where 'S' marks the start, '^' marks splitters.

    Returns:
        Total number of split events (hits on '^' characters).
    """
    width = len(manifold[0])

    # Find starting position
    index_s = min([idx for idx, x in enumerate(manifold[0]) if x == "S"])

    # Track beam positions as a set (beams at same position merge)
    beam_positions = {index_s}
    total_hits = 0

    # Process each row after the first
    for row in manifold[1:]:
        new_positions = set()
        for pos in beam_positions:
            if not (0 <= pos < width):
                continue
            if row[pos] == '^':
                # Count this hit
                total_hits += 1
                # Split: beam goes both left and right
                new_positions.add(pos - 1)
                new_positions.add(pos + 1)
            else:
                # Continue straight
                new_positions.add(pos)
        # Filter out of bounds positions
        beam_positions = {p for p in new_positions if 0 <= p < width}

    return total_hits


def parse(input_text: str) -> List[List[str]]:
    """Parse the puzzle input."""
    
    mainifold = []
    for line in input_text.splitlines():
        if line.strip() != "":
            mainifold.append([c for c in line.strip()])
    return mainifold


def part1(input_text: str) -> int:
    """Solve part 1."""
    manifold = parse(input_text)
    return num_splits(manifold)


def part2(input_text: str) -> int:
    """Solve part 2."""
    manifold = parse(input_text)
    return num_splits_quantum(manifold)


if __name__ == "__main__":
    with open("puzzle_input/day07.txt") as f:
        input_text = f.read()
    print(f"Part 1: {part1(input_text)}")
    print(f"Part 2: {part2(input_text)}")
