from utils.api import get_input
from datetime import datetime


def rotate90(map: list[str]) -> list[str]:
    return ["".join([map[j][i] for j in range(len(map))]) for i in range(len(map[0]))]


def contains(small, big):
    for i in range(len(big) - len(small) + 1):
        for j in range(len(small)):
            if big[i + j] != small[j]:
                break
        else:
            return i, i + len(small)
    return False


def drop(map: list[str], reserve: bool) -> list[str]:
    rotated_map = rotate90(map)
    result_map = []

    for line in rotated_map:
        result_line = ""
        splited_line = line.replace("#", "?#?").split("?")
        for sub_line in splited_line:
            if len(sub_line) == 0:
                continue
            elif sub_line[0] == "#":
                result_line += sub_line
            else:
                result_line += "".join(sorted(sub_line, reverse=reserve))
        result_map.append(result_line)

    return result_map


def drop_top_left(map: list[str]) -> list[str]:
    return drop(map, True)


def drop_bottom_right(map: list[str]) -> list[str]:
    return drop(map, False)


def get_weight(map: list[str]) -> int:
    total = 0
    for index, line in enumerate(result_map[::-1]):
        total += (index + 1) * line.count("O")
    return total


max_step = 1000000000
input_str = get_input(14)
result_map = input_str.splitlines()
weight_list = []
cycle_list = []
cycle_start_map = []

for i in range(1, max_step + 1):
    result_map = drop_top_left(result_map)
    result_map = drop_top_left(result_map)
    result_map = drop_bottom_right(result_map)
    result_map = drop_bottom_right(result_map)
    # hope for a cycle
    weight = get_weight(result_map)
    if weight in weight_list:
        # maybe a cycle ?
        if (
            len(cycle_list) > 0
            and weight == cycle_list[0]
            and result_map == cycle_start_map
        ):
            # found one !
            cycle_size = len(cycle_list)
            step_before_start_of_cycle = len(weight_list)
            step_of_cycle_at_max_step = (
                max_step - step_before_start_of_cycle
            ) % cycle_size
            print(cycle_list[step_of_cycle_at_max_step - 1])
            break
            # weight_list += cycle_list
            # cycle_list = [weight]

        else:
            if len(cycle_list) == 0:
                cycle_start_map = result_map
            cycle_list.append(weight)
            if not contains(cycle_list, weight_list):
                # not a cycle
                weight_list += cycle_list
                cycle_list = []
    else:
        weight_list.append(weight)
