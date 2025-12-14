"""Advent of Code 2025 - Day 5"""

import networkx as nx 


def parse(input_text: str) -> nx.DiGraph:
    """Parse the puzzle input."""

    G = nx.DiGraph()
    for line in input_text.splitlines():
        if ":" not in line:
            continue

        source, dests_str = line.split(":")

        if source not in G:
            G.add_node(source)

        for dest in dests_str.strip().split(" "):
            if dest not in G:
                G.add_node(dest)
            G.add_edge(source, dest)

    return G
            

def part1(input_text: str) -> int:
    """Solve part 1."""
    G = parse(input_text)
    path_generator = nx.all_simple_paths(G, source='you', target='out')
    return len(list(path_generator))


def part2(input_text: str) -> int:
    """Solve part 2."""
    return 0


if __name__ == "__main__":
    with open("puzzle_input/day11.txt") as f:
        input_text = f.read()
    print(f"Part 1: {part1(input_text)}")
    print(f"Part 2: {part2(input_text)}")
