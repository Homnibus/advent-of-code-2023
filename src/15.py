from utils.api import get_input


def hash(string: str) -> int:
    total = 0
    for char in string:
        total += ord(char)
        total *= 17
        total = total % 256
    return total


input_str_list = get_input(15).split(",")

box_list = [{} for i in range(256)]
for string in input_str_list:
    if string[-1] == "-":
        # dash operation
        lens_label = string[:-1]
        box_id = hash(lens_label)
        box = box_list[box_id]
        if lens_label in box:
            box.pop(lens_label)
    else:
        lens_label, lens_focal = string.split("=")
        box_id = hash(lens_label)
        box = box_list[box_id]
        box[lens_label] = lens_focal

total = 0
for index, box in enumerate(box_list):
    i = 1
    for focal in box.values():
        total += (index + 1) * i * int(focal)
        i+=1

print(total)
