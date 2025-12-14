"""Tests for Day 10."""

from solutions.day10 import part1, part2, parse, apply_button, find_minimal_sequence, find_minimal_sequence_joltage

# Paste the example input from the puzzle description here
EXAMPLE = """
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""


def test_button_push():
    assert apply_button('#.....', (0,3,4)) == '...##.'


def test_find_minmal_sequence():
    machines = parse(EXAMPLE)
    assert len(find_minimal_sequence(machines[0].indicator_lights, machines[0].buttons)) == 2


def test_find_minmal_sequence_joltage():
    machines = parse(EXAMPLE)
    assert find_minimal_sequence_joltage(machines[0].joltage, machines[0].buttons) == 10


def test_parse():
    machines = parse(EXAMPLE)
    assert machines[0].indicator_lights == ['.', '#', '#', '.']
    assert machines[1].joltage == [7, 5, 12, 7, 2]
    assert machines[1].buttons[1] == (2,3)


def test_part1():
    """Test part 1 with example input."""
    assert part1(EXAMPLE) == 7


def test_part2():
    """Test part 2 with example input."""
    assert part2(EXAMPLE) == 33

