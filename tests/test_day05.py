"""Tests for Day 5."""

from solutions.day05 import part1, part2, parse, fresh_ingredient 

# Paste the example input from the puzzle description here
EXAMPLE = """
3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""


def test_fresh_ingredient():
    """Test count adjacent function"""
    fresh_ranges, _ = parse(EXAMPLE)
    assert fresh_ingredient(fresh_ranges, 1) == False
    assert fresh_ingredient(fresh_ranges, 5) == True
    assert fresh_ingredient(fresh_ranges, 8) == False
    assert fresh_ingredient(fresh_ranges, 11) == True
    assert fresh_ingredient(fresh_ranges, 17) == True
    assert fresh_ingredient(fresh_ranges, 32) == False


def test_part1():
    """Test part 1 with example input."""
    # Update expected value from puzzle description
    assert part1(EXAMPLE) == 3


def test_part2():
    """Test part 2 with example input."""
    assert part2(EXAMPLE) == 14

