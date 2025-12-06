"""Advent of Code 2025 - Day 1"""


def rotate_dial(starting_position: int, direction: str, distance: int) -> int:

    if direction not in ['R', 'L']:
        raise ValueError(f"direction must be either R or L, {direction}")

    ending_position = starting_position
    distance = -1 * distance if direction == 'L' else distance
    
    if ending_position + distance > 99:
        distance = ending_position + distance - 99 -1
        ending_position = 0 
        return rotate_dial(ending_position, direction, abs(distance))
    
    elif ending_position + distance < 0:
        distance = ending_position + distance + 1
        ending_position = 99
        return rotate_dial(ending_position, direction, abs(distance))
    
    else:
        return ending_position + distance 


def rotate_dial_count_zero(starting_position: int, direction: str, distance: int) -> int:

    if direction not in ['R', 'L']:
        raise ValueError(f"direction must be either R or L, {direction}")

    if distance == 0:
        return 0

    ending_position = starting_position
    distance = -1 * distance if direction == 'L' else distance
    
    if ending_position + distance > 99:
        distance = ending_position + distance - 100
        ending_position = 0 
        return 1 + rotate_dial_count_zero(ending_position, direction, abs(distance))
    
    elif ending_position + distance < 0:
        distance = ending_position + distance + 1
        ending_position = 99
        return (1 if starting_position != 0 else 0) + rotate_dial_count_zero(ending_position, direction, abs(distance))
    
    else:
        return int(ending_position + distance == 0)


def parse(input_text: str):
    """Parse the puzzle input."""
    return input_text.strip().split("\n")


def part1(input_text: str) -> int:
    """Solve part 1."""
    data = parse(input_text)
    password = 0
    starting_position = 50
    for movement in data:
        movement = movement.strip()
        starting_position = rotate_dial(starting_position, movement[0], int(movement[1:]))
        if starting_position == 0:
            password = password + 1 
    
    return password


def part2(input_text: str) -> int:
    """Solve part 2."""
    data = parse(input_text)
    password = 0
    starting_position = 50
    for movement in data:
        movement = movement.strip()
        password = password + rotate_dial_count_zero(starting_position, movement[0], int(movement[1:]))
        starting_position = rotate_dial(starting_position, movement[0], int(movement[1:]))

    return password    


if __name__ == "__main__":
    with open("puzzle_input/day01.txt") as f:
        input_text = f.read()
    print(f"Part 1: {part1(input_text)}")
    print(f"Part 2: {part2(input_text)}")
