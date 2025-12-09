"""Tests for Day 9."""

from solutions.day09 import part1, part2

# Paste the example input from the puzzle description here
EXAMPLE = """
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""

def test_part1():
    """Test part 1 with example input."""
    # Update expected value from puzzle description
    assert part1(EXAMPLE) == 50


def test_part2():
    """Test part 2 with example input."""
    assert part2(EXAMPLE) == 24

