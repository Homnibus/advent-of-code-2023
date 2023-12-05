import re
from utils.api import get_input

input_str = get_input(5)


def extract_convertion_table(split_inputs: list[str], rank: int) -> list[list[int]]:
    convertion_str = split_inputs[rank].splitlines()[1:]
    convertion_values = list(
        map(
            lambda x: list(map(lambda x: int(x), re.findall(r"([0-9]+)", x))),
            convertion_str,
        )
    )
    # add end limit
    convertion_values.append(
        [-1, 9999999999999999999999999999999999999999999999999999999999999999, 0]
    )
    convertion_values.sort(key=lambda values: values[1])
    return convertion_values

def translate(seeds: list[int], convertion_table: list[list[int]]) -> list[int]:
    translated_seeds: list[int] = []
    ct_index = 0
    for seed in seeds:
        while seed > (
            convertion_table[ct_index][1] + convertion_table[ct_index][2] - 1
        ):
            ct_index += 1
        else:
            if seed < (convertion_table[ct_index][1]):
                translated_seeds.append(seed)
            else:
                translated_seeds.append(
                    seed + convertion_table[ct_index][0] - convertion_table[ct_index][1]
                )
    translated_seeds.sort()
    return translated_seeds


split_inputs = input_str.split("\n\n")

seed_str = split_inputs[0].split(":")[1]
seeds = re.findall(r"([0-9]+)", seed_str)
seeds = list(map(lambda x: int(x), seeds))
seeds.sort()

convertion_table_list = [extract_convertion_table(split_inputs, i) for i in range(1, 8)]

current_category_values = seeds

for convertion_table in convertion_table_list:
    current_category_values = translate(current_category_values, convertion_table)


print(current_category_values[0])
