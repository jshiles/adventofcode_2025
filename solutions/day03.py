"""Advent of Code 2025 - Day 3"""

import numpy as np 
from typing import List


def max_joltage(bank: str, num_batteries: int = 2) -> int:
    """Find the largest int of size num_batteries in the bank str"""
    batteries = [int(x) for x in bank]

    batteries_idx: List[int] = []
    current_idx = 0
    joltage = 0

    for nbattery in range(num_batteries, 0, -1):
        max_search_idx = -1 * (nbattery-1) if nbattery-1 > 0 else len(batteries)
        max_idx = np.argmax(batteries[current_idx : max_search_idx])
        batteries_idx.append(max_idx + current_idx)
        
        current_idx = current_idx + max_idx + 1 

    batteries_idx = list(reversed(batteries_idx))

    for digit in range(0, len(batteries_idx)):
        joltage = joltage + 10**digit * batteries[batteries_idx[digit]]   

    return joltage


def parse(input_text: str):
    """Parse the puzzle input."""
    return input_text.strip().split("\n")


def part1(input_text: str) -> int:
    """Solve part 1."""
    data = parse(input_text)
    sum_joltage = 0
    for bank in data:
        sum_joltage = sum_joltage + max_joltage(bank.strip())
    return sum_joltage


def part2(input_text: str) -> int:
    """Solve part 2."""
    data = parse(input_text)
    sum_joltage = 0
    for bank in data:
        sum_joltage = sum_joltage + max_joltage(bank.strip(), 12)
    return sum_joltage


if __name__ == "__main__":
    with open("puzzel_input/day03.txt") as f:
        input_text = f.read()
    print(f"Part 1: {part1(input_text)}")
    print(f"Part 2: {part2(input_text)}")
