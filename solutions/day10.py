"""Advent of Code 2025 - Day 10"""


import re
from collections import deque
from dataclasses import dataclass
from typing import List, Optional, Tuple

import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds


@dataclass(frozen=True)
class Machine:
    indicator_lights: list[str]
    buttons: List[Tuple[int, ...]]
    joltage: List[int]


def apply_button(state: str, button: Tuple[int, ...]) -> str:
    """
    Apply a button push to a state string, returning the new state.

    Args:
        state: Current state string of indicator lights ('.' or '#')
        button: Tuple of indices to toggle

    Returns:
        New state string after toggling the specified indices
    """
    lights = list(state)
    for idx in button:
        lights[idx] = '#' if lights[idx] == '.' else '.'
    return ''.join(lights)


def find_minimal_sequence(
    target: List[str], buttons: List[Tuple[int, ...]]
) -> Optional[List[int]]:
    """
    Find the minimal sequence of button pushes to transform an all-'.' state
    into the target indicator_lights state using BFS.

    Args:
        target: The target indicator lights configuration
        buttons: List of button tuples, where each tuple contains indices to toggle

    Returns:
        A list of button indices representing the minimal sequence, or None if impossible
    """
    target_str = ''.join(target)
    start_str = '.' * len(target)

    if start_str == target_str:
        return []

    # BFS: queue contains (current_state, sequence_of_button_indices)
    queue = deque([(start_str, [])])
    visited = {start_str}

    while queue:
        current_state, sequence = queue.popleft()

        for button_idx, button in enumerate(buttons):
            new_state = apply_button(current_state, button)

            if new_state == target_str:
                return sequence + [button_idx]

            if new_state not in visited:
                visited.add(new_state)
                queue.append((new_state, sequence + [button_idx]))

    return None  # No solution found


def find_minimal_sequence_joltage(target: List[int], buttons: List[Tuple[int, ...]]) -> Optional[int]:
    """
    Find the minimal number of button presses to reach the target joltage values.

    Solves the system A @ x = target where x >= 0 and minimizes sum(x).
    Uses Mixed Integer Linear Programming (MILP) for efficient solving.

    Args:
        target: The target joltage values for each position
        buttons: List of button tuples, where each tuple contains indices to increment

    Returns:
        The minimal total number of button presses, or None if impossible
    """
    if all(t == 0 for t in target):
        return 0

    n_buttons = len(buttons)
    n_positions = len(target)

    # Build effect matrix A: A[pos][btn] = 1 if button affects position
    # We want A @ x = target (equality constraint)
    A_eq = np.zeros((n_positions, n_buttons), dtype=np.float64)
    for btn_idx, button in enumerate(buttons):
        for pos in button:
            if pos < n_positions:
                A_eq[pos, btn_idx] = 1

    b_eq = np.array(target, dtype=np.float64)

    # Check if any position has no buttons that can reach it
    for pos in range(n_positions):
        if b_eq[pos] > 0 and A_eq[pos].sum() == 0:
            return None

    # Objective: minimize sum of all button presses
    c = np.ones(n_buttons)

    # Bounds: x >= 0, x <= max(target) (upper bound for efficiency)
    upper_bound = max(target) if target else 0
    bounds = Bounds(lb=0, ub=upper_bound)

    # Equality constraint: A @ x = b
    constraints = LinearConstraint(A_eq, b_eq, b_eq)

    # All variables are integers
    integrality = np.ones(n_buttons)

    # Solve using MILP
    result = milp(c, constraints=constraints, bounds=bounds, integrality=integrality)

    if result.success and result.x is not None:
        # Round to ensure integer (should already be, but float precision)
        solution = np.round(result.x).astype(int)
        # Verify the solution
        if np.allclose(A_eq @ solution, b_eq):
            return int(solution.sum())

    return None


def parse(input_text: str) -> List[Machine]:
    machines: List[Machine] = []
    pattern = r'\[([^\]]+)\]\s+((?:\([^)]+\)\s*)+)\{([^}]+)\}'

    for line in input_text.splitlines():
        if not line.strip():
            continue

        match = re.match(pattern, line)
        if match:
            # Parse indicator lights as list of characters
            indicator_lights = list(match.group(1))

            # Parse buttons - find all tuples
            buttons_str = match.group(2)
            buttons = []
            for button_match in re.findall(r'\(([^)]+)\)', buttons_str):
                button_tuple = tuple(int(x) for x in button_match.split(','))
                buttons.append(button_tuple)

            # Parse joltage as list of integers
            joltage = [int(x) for x in match.group(3).split(',')]

            machines.append(Machine(indicator_lights, buttons, joltage))

    return machines


def part1(input_text: str) -> int:
    """Solve part 1."""
    machines = parse(input_text)
    return sum([len(find_minimal_sequence(x.indicator_lights, x.buttons)) for x in machines])


def part2(input_text: str) -> int:
    """Solve part 2."""
    machines = parse(input_text)
    return sum([find_minimal_sequence_joltage(x.joltage, x.buttons) for x in machines])


if __name__ == "__main__":
    with open("puzzle_input/day10.txt") as f:
        input_text = f.read()
    print(f"Part 1: {part1(input_text)}")
    print(f"Part 2: {part2(input_text)}")
