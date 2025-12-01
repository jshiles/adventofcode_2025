"""Tests for Day 1."""

from solutions.day01 import part1, part2, rotate_dial, rotate_dial_count_zero

# Paste the example input from the puzzle description here
EXAMPLE = """\
"""


def test_rotate_dial():
    assert rotate_dial(11, 'R', 8) == 19
    assert rotate_dial(19, 'L', 19) == 0 
    assert rotate_dial(0, 'L', 1) == 99
    assert rotate_dial(50, 'L', 68) == 82
    assert rotate_dial(52, 'R', 48) == 0
    assert rotate_dial(50, 'R', 95) == 45
    assert rotate_dial(50, 'R', 194) == 44



def test_rotate_dial_count_zero():
    assert rotate_dial_count_zero(50, 'L', 68) == 1
    assert rotate_dial_count_zero(82, 'L', 30) == 0
    assert rotate_dial_count_zero(52, 'R', 48) == 1
    assert rotate_dial_count_zero(0, 'L', 5) == 0 
    assert rotate_dial_count_zero(95, 'R', 60) == 1 
    assert rotate_dial_count_zero(50, 'L', 1000) == 10


def test_part1():
    """Test part 1 with example input."""
    # Update expected value from puzzle description
    input = "L68\nL30\nR48\nL5\nR60\nL55\nL1\nL99\nR14\nL82"
    assert part1(input) == 3


def test_part2():
    """Test part 2 with example input."""
    input = "L68\nL30\nR48\nL5\nR60\nL55\nL1\nL99\nR14\nL82"
    assert part2(input) == 6
