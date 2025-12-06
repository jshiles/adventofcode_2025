"""Tests for Day 6."""

from solutions.day06 import part1, part2, transform_numbers

# Paste the example input from the puzzle description here
EXAMPLE = """
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
"""

def test_transform_numbers():
    assert transform_numbers(['64 ', '23 ', '314']) == [4, 431, 623]
    assert transform_numbers([' 51', '387', '215']) == [175, 581, 32]
    assert transform_numbers(['328', '64 ', '98 ']) == [8, 248, 369]
    assert transform_numbers(['123', ' 45', '  6']) == [356, 24, 1]


def test_part1():
    """Test part 1 with example input."""
    # Update expected value from puzzle description
    assert part1(EXAMPLE) == 4277556


def test_part2():
    """Test part 2 with example input."""
    assert part2(EXAMPLE) == 3263827

