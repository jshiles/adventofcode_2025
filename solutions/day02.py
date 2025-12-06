"""Advent of Code 2025 - Day 2"""

from typing import List 
from functools import lru_cache


def invalid_productid(id: int) -> bool:
    """ """
    s = str(id)
    if len(s) % 2 != 0:
        return False 

    mid = len(s) // 2
    return int(s[:mid]) == int(s[mid:])


def invalid_sequences(start: int, end: int) -> List[int]:
    """ 
    Check for repeated sequences in the range that have invalid productids
    """
    invalid = []
    for x in range(start, end + 1):
        if invalid_productid(x):
            invalid.append(x)
    return invalid


@lru_cache
def get_subsequences(sequence: int) -> List[List[int]]:
    """
    Break a sequence of digits into all possible chunk sizes that divide evenly.
    Returns a list of lists, where each inner list contains the sequence
    split into equal-sized integer chunks (with 2 or more chunks).
    Example: "824824824" -> [[824, 824, 824], [8, 2, 4, 8, 2, 4, 8, 2, 4]]
    Example: "12341234" -> [[1234, 1234], [12, 34, 12, 34], [1, 2, 3, 4, 1, 2, 3, 4]]
    """
    s = str(sequence)
    n = len(s)

    results = []
    # Find all chunk sizes that divide n evenly and produce at least 2 chunks
    for chunk_size in range(n // 2, 0, -1):
        if n % chunk_size == 0 and n // chunk_size >= 2:
            chunks = [int(s[i:i + chunk_size]) for i in range(0, n, chunk_size)]
            results.append(chunks)

    return results


def invalid_subsequences(start: int, end: int) -> List[int]:
    invalid = []
    for x in range(start, end + 1):
        for subsequence in get_subsequences(x):
            if len(set(subsequence)) <= 1:
                invalid.append(x)
                break
 
    return invalid



def parse(input_text: str):
    """Parse the puzzle input."""
    return input_text.strip().split(",")


def part1(input_text: str) -> int:
    """Solve part 1."""
    data = parse(input_text)
    sum_invalid_productids = 0
    for x in data:
        start, end = x.split('-')
        sum_invalid_productids = sum_invalid_productids + sum(invalid_sequences(int(start), int(end)))
    return sum_invalid_productids


def part2(input_text: str) -> int:
    """Solve part 2."""
    data = parse(input_text)
    sum_invalid_productids = 0 
    for x in data:
        start, end = x.split('-')
        sum_invalid_productids = sum_invalid_productids + sum(invalid_subsequences(int(start), int(end)))
    return sum_invalid_productids


if __name__ == "__main__":
    with open("puzzle_input/day02.txt") as f:
        input_text = f.read()
    print(f"Part 1: {part1(input_text)}")
    print(f"Part 2: {part2(input_text)}")
