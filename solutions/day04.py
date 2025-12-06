"""Advent of Code 2025 - Day 4"""

from typing import List


def count_adjacent(board: List[List[str]], row: int, col: int) -> int:
    """ """
    if len(board) == 0:
        raise ValueError("Invalid Board")

    num_adjacent = 0
    for i in range(row - 1, row + 2):
        for j in range (col -1, col + 2): 
            if (
                    0 <= i < len(board) and 
                    0 <= j < len(board[0]) and 
                    not (i == row and j == col) and
                    board[i][j] != '.'
                ):
                num_adjacent += 1 
    return num_adjacent


def parse(input_text: str) -> List[List[str]]:
    """Parse the puzzle input."""
    board: List[List[str]] = []
    for line in input_text.strip().split("\n"):
        board.append([str(c) for c in line])
    return board


def part1(input_text: str) -> int:
    """Solve part 1."""
    board = parse(input_text)
    reachable = 0
    for i, row in enumerate(board):
        for j, ch in enumerate(row):
            if ch == '@' and count_adjacent(board, i, j) < 4:
                reachable += 1 

    return reachable


def part2(input_text: str) -> int:
    """Solve part 2."""
    
    board = parse(input_text)
    reachable = 0
    reachable_found = True

    while reachable_found:
        iteration_reachable = 0
        for i, row in enumerate(board):
            for j, ch in enumerate(row):
                if ch == '@' and count_adjacent(board, i, j) < 4:
                    iteration_reachable += 1 
                    board[i][j] = 'x'

        if iteration_reachable == 0:
            reachable_found = False 
        else:
            reachable += iteration_reachable
            for i, row in enumerate(board):
                for j, ch in enumerate(row):
                    if ch == 'x':
                        board[i][j] = '.'

    return reachable



if __name__ == "__main__":
    with open("puzzle_input/day04.txt") as f:
        input_text = f.read()
    print(f"Part 1: {part1(input_text)}")
    print(f"Part 2: {part2(input_text)}")
