import re
from utils.api import get_input

def rotate(map: list[str]) -> list[str]:
    return [''.join([map[j][i] for j in range(len(map))]) for i in range(len(map[0]))]

def get_lines_to_expand(map: list[str]) -> list[int]:
    lines_to_expand:list[int] = []
    for line_index,line in enumerate(map):
        if "#" not in line:
            lines_to_expand.append(line_index)
    return lines_to_expand

def get_columns_to_expand(map: list[str]) -> list[int]:
    map_rotated_90 = rotate(map)
    return get_lines_to_expand(map_rotated_90)

input_str = get_input(11)
map = input_str.splitlines()
lines_to_expand = get_lines_to_expand(map)
columns_to_expand = get_columns_to_expand(map)

expand_value = 1000000

galaxys:list[list[int]] = []

for line_index, line in enumerate(map):
    for match in re.finditer(r"#", line):
        galaxys.append([line_index,match.start()])
    
total = 0

while len(galaxys) > 0:
    current_galaxy = galaxys.pop(0)
    for galaxy in galaxys:
        line_expand = [line for line in lines_to_expand if (current_galaxy[0] > line > galaxy[0]) or (current_galaxy[0] < line < galaxy[0]) ]
        column_expand = [column for column in columns_to_expand if (current_galaxy[1] > column > galaxy[1]) or (current_galaxy[1] < column < galaxy[1]) ]
        total += abs(current_galaxy[0] - galaxy[0]) + len(line_expand) * (expand_value - 1)  + abs(current_galaxy[1] - galaxy[1]) + len(column_expand) * (expand_value - 1)
        
print(total)