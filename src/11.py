import re
from utils.api import get_input

def rotate(map: list[str]) -> list[str]:
    return [''.join([map[j][i] for j in range(len(map))]) for i in range(len(map[0]))]

def add_padding(map: list[str]) -> list[str]:
    padded_map = map.copy()
    for i in range(0, len(padded_map)):
        padded_map[i] = "." + padded_map[i] + "."
    padded_map.append("." * len(map[0]))
    padded_map.insert(0, "." * len(map[0]))
    return padded_map

def expend_empty_lines(map: list[str]) -> list[str]:
    line_expended_map: list[str] = []
    for line in map:
        if "#" not in line:
            line_expended_map.append("." * len(map[0]))
        line_expended_map.append(line)
    return line_expended_map
    
def expend_empty_col(map: list[str]) -> list[str]:
    map_rotated_90 = rotate(map)
    col_expended_map_rotated_90 = expend_empty_lines(map_rotated_90)
    col_expended_map = rotate(col_expended_map_rotated_90)
    return col_expended_map

input_str = get_input(11)
map = input_str.splitlines()
padded_map = add_padding(map)
expended_map = add_padding(expend_empty_lines(expend_empty_col(map)))

galaxys:list[list[int]] = []

for line_index, line in enumerate(expended_map):
    for match in re.finditer(r"#", line):
        galaxys.append([line_index,match.start()])
    
total = 0

while len(galaxys) > 0:
    current_galaxy = galaxys.pop(0)
    for galaxy in galaxys:
        total += abs(current_galaxy[0] - galaxy[0]) + abs(current_galaxy[1] - galaxy[1])
        
print(total)