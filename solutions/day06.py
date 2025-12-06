"""Advent of Code 2025 - Day 6"""

import pandas as pd
from io import StringIO
from typing import List
from itertools import pairwise


def calculate_solution(row: pd.Series):
    """
    Calculates the sum or product of the numeric columns
    based on the operator in the 'operation' column.
    """
    # Select the numerical columns (all except 'operation')
    numbers = row.drop('operation').tolist()
    operator = row['operation']

    if operator == '+':
        # Sum the numbers
        return sum(numbers)
    elif operator == '*':
        # Multiply the numbers
        solution = 1
        for num in numbers:
            solution *= num
        return solution
    else:
        # Handle other operators/errors if needed
        return None 


def solve_problems(df: pd.DataFrame) -> int:
    df['solution'] = df.apply(calculate_solution, axis=1)
    return df['solution'].sum()


def part1(input_text: str) -> int:
    """Solve part 1."""
    df = pd.read_csv(StringIO(input_text), header=None, sep=r"\s+", engine="python").T

    last_col_index = df.columns[-1]
    df = df.rename(columns={last_col_index: 'operation'})

    columns_to_cast = df.columns[:-1]
    df[columns_to_cast] = df[columns_to_cast].astype(int)
    
    return solve_problems(df)


def transform_numbers(numbers: List[str]) -> List[int]:
    """
    Each number is given in its own column, with the most significant digit at
    the top and the least significant digit at the bottom.
    ['64 ', '23 ', '314'] -> [4, 431, 623]
    """
    mlength = max([len(x) for x in numbers])
    
    new_numbers = []
    for i in range(mlength):
        digits = [n[i] for n in numbers]
        try:
            number = int("".join(digits).strip())
        except ValueError:
            continue
        new_numbers.append(number)

    return new_numbers[::-1]


def calculate_solution_p2(row: pd.Series):
    operator = row['operation'].strip()
    numbers = row.drop('operation').tolist()
    new_numbers = transform_numbers(numbers)

    if operator == '+':
        return sum(new_numbers)
    elif operator == '*':
        solution = 1
        for num in new_numbers:
            solution *= num
        return solution
    else:
        return None 


def solve_problems_p2(df: pd.DataFrame) -> int:
    df['solution'] = df.apply(calculate_solution_p2, axis=1)
    return df['solution'].sum()


def part2(input_text: str) -> int:
    """Solve part 2."""
    lines = input_text.lstrip().splitlines()
    operator_line = lines[-1]
    operator_idxs = [idx for idx, ch in enumerate(operator_line) if ch != ' ']

    number_lines = lines[:-1]
    rows = []
    for line in number_lines:
        numbers = []
        for p_idx, c_idx in pairwise(operator_idxs):
            numbers.append(line[p_idx: c_idx-1])
        numbers.append(line[operator_idxs[-1]:])
        rows.append(numbers)

    rows.append([ch for ch in operator_line if ch != ' '])

    df = pd.DataFrame(rows).T
    df.dropna(inplace=True)

    last_col_index = df.columns[-1]
    df = df.rename(columns={last_col_index: 'operation'})

    print(df)

    return solve_problems_p2(df)


if __name__ == "__main__":
    with open("puzzle_input/day06.txt") as f:
        input_text = f.read()
    print(f"Part 1: {part1(input_text)}")
    print(f"Part 2: {part2(input_text)}")
