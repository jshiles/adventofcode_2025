"""Tests for Day 3."""

from solutions.day03 import part1, part2, max_joltage

input = """987654321111111
811111111111119
234234234234278
818181911112111
"""

def test_max_joltage():
    data = input.strip().split("\n")
    assert max_joltage(data[0].strip()) == 98 
    assert max_joltage(data[1].strip()) == 89 
    assert max_joltage(data[2].strip()) == 78 
    assert max_joltage(data[3].strip()) == 92 

    # part 2 
    assert max_joltage(data[0].strip(), 12) == 987654321111 
    assert max_joltage(data[1].strip(), 12) == 811111111119
    assert max_joltage(data[2].strip(), 12) == 434234234278 
    assert max_joltage(data[3].strip(), 12) == 888911112111 


def test_part1():
    """Test part 1 with example input."""
    # Update expected value from puzzle description
    assert part1(input) == 357


def test_part2():
    """Test part 2 with example input."""
    assert part2(input) == 3121910778619


