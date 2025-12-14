"""Advent of Code 2025 - Day 11"""

from typing import Dict, List

import networkx as nx


def count_paths_with_intermediates(
    G: nx.DiGraph, source: str, target: str, intermediates: List[str]
) -> int:
    """
    Count simple paths from source to target that pass through all intermediate nodes.

    Since the order of visiting intermediates matters, this function checks both
    possible orderings (A->B and B->A) and sums the valid path counts.

    Args:
        G: A directed graph to search for paths.
        source: The starting node for paths.
        target: The ending node for paths.
        intermediates: A list of exactly two nodes that must be visited.

    Returns:
        The total count of simple paths passing through all intermediates.
    """
    node_a = intermediates[0]
    node_b = intermediates[1]

    # Order 1: source -> A -> B -> target
    count_order_1 = count_waypoint_paths_dag(G, [source, node_a, node_b, target])

    # Order 2: source -> B -> A -> target
    count_order_2 = count_waypoint_paths_dag(G, [source, node_b, node_a, target])

    return count_order_1 + count_order_2


def count_paths_dag(G: nx.DiGraph, source: str, target: str) -> int:
    """
    Count all paths from source to target in a DAG using DP.

    In a DAG, all paths are simple (no cycles means no revisiting nodes).
    Uses reverse topological order DP: paths_to[node] = sum(paths_to[successor]).

    Args:
        G: A directed acyclic graph.
        source: Starting node.
        target: Ending node.

    Returns:
        Number of paths from source to target.
    """
    # DP from target backwards: paths_to_target[node] = number of paths from node to target
    paths_to_target: Dict[str, int] = {target: 1}

    # Process in reverse topological order
    topo_order = list(nx.topological_sort(G))

    for node in reversed(topo_order):
        if node == target:
            continue
        count = 0
        for successor in G.successors(node):
            count += paths_to_target.get(successor, 0)
        if count > 0:
            paths_to_target[node] = count

    return paths_to_target.get(source, 0)


def count_waypoint_paths_dag(G: nx.DiGraph, waypoints: List[str]) -> int:
    """
    Count paths through waypoints in a DAG.

    Since a DAG has no cycles, all paths are simple. We can multiply path counts
    between consecutive waypoints to get total paths through all waypoints.

    Args:
        G: A directed acyclic graph.
        waypoints: Ordered list of nodes [start, w1, w2, ..., end].

    Returns:
        Number of paths visiting all waypoints in order.
    """
    if len(waypoints) < 2:
        return 1 if len(waypoints) == 1 else 0

    total = 1
    for i in range(len(waypoints) - 1):
        segment_count = count_paths_dag(G, waypoints[i], waypoints[i + 1])
        if segment_count == 0:
            return 0
        total *= segment_count

    return total


def parse(input_text: str) -> nx.DiGraph:
    """
    Parse the puzzle input into a directed graph.

    Expects input in the format "source: dest1 dest2 dest3" per line,
    where each line defines edges from source to each destination.

    Args:
        input_text: Raw puzzle input with adjacency list format.

    Returns:
        A directed graph with nodes and edges from the input.
    """

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
    return sum(1 for _ in nx.all_simple_paths(G, source='you', target='out'))


def part2(input_text: str) -> int:
    """Solve part 2."""
    G = parse(input_text)
    return count_paths_with_intermediates(G, 'svr', 'out', ['fft', 'dac'])


if __name__ == "__main__":
    with open("puzzle_input/day11.txt") as f:
        input_text = f.read()
    print(f"Part 1: {part1(input_text)}")
    print(f"Part 2: {part2(input_text)}")
