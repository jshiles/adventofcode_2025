"""Tests for Day 11."""

from solutions.day11 import part1, part2 

# Paste the example input from the puzzle description here
EXAMPLE = """
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
"""


def test_part1():
    """Test part 1 with example input."""
    assert part1(EXAMPLE) == 5


def test_part2():
    """Test part 2 with example input."""
    assert part2(EXAMPLE) == 0

