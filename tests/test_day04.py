"""Tests for Day 4."""

from solutions.day04 import part1, part2, parse, count_adjacent

# Paste the example input from the puzzle description here
EXAMPLE = """
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""


def test_count_adjacent():
    """Test count adjacent function"""
    board = parse(EXAMPLE)

    assert count_adjacent(board, 0, 2) < 4
    assert count_adjacent(board, 0, 3) < 4
    assert count_adjacent(board, 0, 5) < 4
    assert count_adjacent(board, 0, 6) < 4
    assert count_adjacent(board, 0, 7) >= 4
    assert count_adjacent(board, 0, 8) < 4
    assert count_adjacent(board, 1, 0) < 4
    assert count_adjacent(board, 1, 1) >= 4



def test_part1():
    """Test part 1 with example input."""
    # Update expected value from puzzle description
    assert part1(EXAMPLE) == 13


def test_part2():
    """Test part 2 with example input."""
    assert part2(EXAMPLE) == 43

