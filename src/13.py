from dataclasses import dataclass
from utils.api import get_input

@dataclass
class Pattern:
    value:list[str]
    type:int = 0
    symetry_zone:int = -1

def extract_pattern(input_str:str) -> list[Pattern]:
    pattern_list:list[Pattern] = []
    splited_input = input_str.split("\n\n")
    for pattern_str in splited_input:
        pattern_list.append(Pattern(pattern_str.splitlines()))
    return pattern_list

def find_vertical_symmetry(pattern:Pattern):
    for i in range(1,len(pattern.value)-1):
        symmetry_find = True
        for j in range(min(i+1, len(pattern.value)-i)):
            if pattern.value[i+j-1] != pattern.value[i-j]:
                symmetry_find = False
                break
        if symmetry_find:
            pattern.type = 1
            pattern.symetry_zone = i
            break

input_str = get_input(13)
pattern_list = extract_pattern(input_str)

find_vertical_symmetry(pattern_list[0])

print('ok')