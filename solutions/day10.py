"""Advent of Code 2025 - Day 10"""


import re
from collections import deque
from dataclasses import dataclass 
from typing import List, Optional, Tuple


@dataclass(frozen=True)
class Machine:
    indicator_lights: list[str]
    buttons: List[Tuple[int, ...]]
    joltage: List[int]


def apply_button(state: str, button: Tuple[int, ...]) -> str:
    """Apply a button push to a state string, returning the new state."""
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
    Uses bounded search since button press order doesn't matter.
    """
    if all(t == 0 for t in target):
        return 0

    n_buttons = len(buttons)
    n_positions = len(target)

    # Build matrix: effect[btn][pos] = 1 if button affects position, else 0
    effect = [[0] * n_positions for _ in range(n_buttons)]
    for btn_idx, button in enumerate(buttons):
        for pos in button:
            if pos < n_positions:
                effect[btn_idx][pos] = 1

    # Check if any position has no buttons that can reach it
    for pos, t in enumerate(target):
        if t > 0 and not any(effect[btn][pos] for btn in range(n_buttons)):
            return None

    # Upper bound: max presses of any single button is max(target)
    max_presses = max(target) if target else 0

    # DFS with pruning: determine count for each button
    def solve(btn_idx: int, remaining: List[int], total_presses: int) -> Optional[int]:
        if btn_idx == n_buttons:
            return total_presses if all(r == 0 for r in remaining) else None

        # Prune: if any remaining is negative, invalid
        if any(r < 0 for r in remaining):
            return None

        best = None
        # Try pressing this button 0 to min(max possible useful presses) times
        max_useful = min(max_presses, min(
            (remaining[pos] for pos in range(n_positions) if effect[btn_idx][pos] == 1),
            default=0
        ))

        for presses in range(max_useful + 1):
            new_remaining = remaining[:]
            for pos in range(n_positions):
                new_remaining[pos] -= effect[btn_idx][pos] * presses

            result = solve(btn_idx + 1, new_remaining, total_presses + presses)
            if result is not None:
                if best is None or result < best:
                    best = result

        return best

    return solve(0, list(target), 0)


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
