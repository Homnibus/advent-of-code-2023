from utils.api import get_input

def rotate(map: list[str]) -> list[str]:
    return [''.join([map[j][i] for j in range(len(map))]) for i in range(len(map[0]))]

input_str = get_input(14)
map = input_str.splitlines()
height = len(map)
width = len(map[0])

rotated_map = rotate(map)

result_map = []

for line in rotated_map:
    result_line = ""
    splited_line = line.replace('#',"?#?").split("?")
    for sub_line in splited_line:
        if len(sub_line) == 0:
            continue
        elif sub_line[0] == "#":
            result_line += sub_line
        else:
            result_line += ''.join(sorted(sub_line,reverse=True))
    result_map.append(result_line)

total = 0

for line in result_map:
    for index,char in enumerate(line[::-1]):
        if char == "O":
            total += 1+index


print(total)

