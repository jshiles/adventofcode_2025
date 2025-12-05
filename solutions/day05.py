"""Advent of Code 2025 - Day 5"""

from typing import List, Tuple


def fresh_ingredient(ranges: List[Tuple[int, int]], id: int) -> bool:
    for low, high in ranges:
        if low <= id <= high:
            return True 
    return False


def combine_ranges(ranges: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """merge overlapping ranges"""

    if len(ranges) <= 1:
        return ranges

    result = [ranges[0]]
    for r in ranges[1:]:
        last = result[-1]
        if r[0] <= last[1] + 1:
            result[-1] = (last[0], max(last[1], r[1]))
        else:
            result.append(r)

    return result


def num_fresh_ingredients(ranges: List[Tuple[int, int]]) -> int:
    """count length ranges, accounting for overlaps"""
    sorted_ranges = sorted(ranges, key=lambda x: x[0])
    new_sorted_ranges = combine_ranges(sorted_ranges)

    ids = 0
    for id_range in new_sorted_ranges:
        ids += id_range[1] - id_range[0] + 1
    
    return ids


def parse(input_text: str) -> Tuple[List[Tuple[int, int]], List[int]]:
    """Parse the puzzle input."""
    
    ranges: List[Tuple[int, int]] = []
    ids: List[int] = []

    for line in input_text.strip().split("\n"):
        if "-" in line:
            low, high = line.strip().split("-")
            ranges.append((min(int(low), int(high)), max(int(low), int(high))))
        elif line.strip() != "":
            ids.append(int(line.strip()))

    return ranges, ids


def part1(input_text: str) -> int:
    """Solve part 1."""
    ranges, ids = parse(input_text)
    fresh = 0
    for id in ids:
        fresh += 1 if fresh_ingredient(ranges, id) else 0

    return fresh


def part2(input_text: str) -> int:
    """Solve part 2."""
    ranges, ids = parse(input_text)
    return num_fresh_ingredients(ranges)


if __name__ == "__main__":
    with open("puzzel_input/day05.txt") as f:
        input_text = f.read()
    print(f"Part 1: {part1(input_text)}")
    print(f"Part 2: {part2(input_text)}")
