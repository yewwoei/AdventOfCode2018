from typing import List
from typing import Tuple
import re
import sys


def part1(input_data: List[str]):

    cloth_grid = generate_grid(input_data)
    length = len(cloth_grid)
    width = len(cloth_grid[0])
    counter = 0
    # then, loop through the entire area and sum up those with two or more.
    for x in range(length):
        for y in range(width):
            if len(cloth_grid[x][y]) > 1:
                counter += 1

    return counter


def generate_grid(input_data):
    # retrieve the maximum dimension of the grid.
    length, width = find_dimensions(input_data)
    # Create a 2d array with empty lists.
    cloth_grid = [[[] for x in range(width)] for y in range(length)]

    for command in input_data:
        cut_id, cut_positions = parse_cuts(command)
        increment_cut(cloth_grid, cut_id, cut_positions)

    return cloth_grid


def find_dimensions(input_data: List[str]):
    final_max_length = 0
    final_max_width = 0
    for command in input_data:
        cut_info = get_cut_information(command)
        x = cut_info[1][0]
        y = cut_info[1][1]
        length = cut_info[2]
        width = cut_info[3]
        current_length = x + length
        current_width = y + width
        if current_length > final_max_length:
            final_max_length = current_length
        if current_width > final_max_width:
            final_max_width = current_width

    return final_max_length, final_max_width


def parse_cuts(cut_design: str):
    # return a list of the cuts in tuples.
    cut_info = get_cut_information(cut_design)

    return cut_info[0], generate_tuples(cut_info[1], cut_info[2], cut_info[3])


def get_cut_information(cut_command: str):
    cut_information = list(map(int, re.findall('\d+', cut_command)))
    cut_id = cut_information[0]
    starting_position = (cut_information[1], cut_information[2])
    length = cut_information[3]
    width = cut_information[4]
    return cut_id, starting_position, length, width


def generate_tuples(starting_position, length: int, width: int):
    ending_length_axis = starting_position[0] + length
    ending_width_axis = starting_position[1] + width

    cuts = []
    for current_length in range(starting_position[0], ending_length_axis):
        for current_width in range(starting_position[1], ending_width_axis):
            cuts.append((current_length, current_width))
    return cuts


def increment_cut(cloth_grid, cut_id, cut_positions: List[Tuple[int, int]]):
    for cut in cut_positions:
        x = cut[0]
        y = cut[1]
        cloth_grid[x][y].append(cut_id)


def part2(input_data: List[str]):
    # generate the cloth grid first.
    cloth_grid = generate_grid(input_data)
    length = len(cloth_grid)
    width = len(cloth_grid[0])

    # after generating cloth grid, iterate starting from the first position.
    unique_claims = get_claim_ids(input_data)
    overlapping_claims = set()
    for x in range(length):
        for y in range(width):
            claims = cloth_grid[x][y]
            if len(claims) != 1:
                for v in claims:
                    overlapping_claims.add(v)

    result = unique_claims - overlapping_claims
    return list(result)[0]


def get_claim_ids(input_data: List[str]):
    # getting the first number from the input data.
    return set(map(get_id, input_data))


def get_id(claim: str):
    return int(re.search(r'\d+', claim).group())


if __name__ == "__main__":
    part1_input = open("input1.txt", 'r')
    print(f"The answer to part 1 is: {part1(part1_input.read().splitlines())}")
    part2_input = open("input1.txt", 'r')
    print(f"The answer to part 2 is: {part2(part2_input.read().splitlines())}")