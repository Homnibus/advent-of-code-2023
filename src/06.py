from cmath import sqrt
from dataclasses import dataclass
from math import ceil, floor
import re
from utils.api import get_input


@dataclass
class Race:
    duration: int
    target_distance: int = 0


def extract_races(input_str: str) -> list[Race]:
    races = []
    splited_input = input_str.splitlines()
    for duration_str in re.findall(r"([0-9]+)", splited_input[0]):
        races.append(Race(int(duration_str)))
    for target_distance_str, race in zip(
        re.findall(r"([0-9]+)", splited_input[1]), races
    ):
        race.target_distance = int(target_distance_str)
    return races


def find_number_of_way_to_win(race: Race) -> int:
    a = -1
    b = race.duration
    c = -race.target_distance
    delta = (b**2) - (4 * a * c)
    solution_1 = (-b - sqrt(delta)) / (2 * a)
    solution_2 = (-b + sqrt(delta)) / (2 * a)
    min = ceil(solution_2.real)
    max = floor(solution_1.real)
    if min == solution_2.real:
        min += 1
    if max == solution_1.real:
        max += -1
    return max - min + 1

input_str = get_input(6)
races = extract_races(input_str)
total = 1
for race in races:
    total *= find_number_of_way_to_win(race)

print(total)
