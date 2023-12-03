from dataclasses import dataclass
from utils.api import get_input
import regex as re

input_str = get_input(3)

schematic_len = 140


@dataclass
class Part:
    value: int
    start: int
    end: int


@dataclass
class SchematicLine:
    line_number: int
    line_value: str
    parts: list[Part]


def is_symbol(character: str) -> bool:
    return character not in ".0123456789"


schematic: list[SchematicLine] = []

# Input parsing
for line_index, line in enumerate(input_str.splitlines()):
    current_part_list = []
    for match in re.finditer(r"[0-9]+", line):
        current_part = Part(int(match.group(0)), match.start(), match.end())
        current_part_list.append(current_part)
    current_schematic_line = SchematicLine(line_index, line, current_part_list)
    schematic.append(current_schematic_line)


# Filter data and add to total
total = 0

for schematic_line in schematic:
    for part in schematic_line.parts:
        # previous line
        if schematic_line.line_number != 0:
            # over the part number
            previous_line = schematic[schematic_line.line_number - 1]
            touched = False
            for character in previous_line.line_value[part.start : part.end]:
                if is_symbol(character):
                    touched = True
                    break
            if touched:
                total += part.value
                continue
            # diagonal before
            if part.start > 0 and is_symbol(previous_line.line_value[part.start - 1]):
                total += part.value
                continue
            # diagonal after
            if part.end < (schematic_len - 1) and is_symbol(
                previous_line.line_value[part.end]
            ):
                total += part.value
                continue

        # current line
        # before
        if part.start > 0 and is_symbol(schematic_line.line_value[part.start - 1]):
            total += part.value
            continue
        # after
        if part.end < (schematic_len - 1) and is_symbol(
            schematic_line.line_value[part.end]
        ):
            total += part.value
            continue

        # next line
        if schematic_line.line_number != (len(schematic) - 1):
            # under the part number
            next_line = schematic[schematic_line.line_number + 1]
            touched = False
            for character in next_line.line_value[part.start : part.end]:
                if is_symbol(character):
                    touched = True
                    break
            if touched:
                total += part.value
                continue
            # diagonal before
            if part.start > 0 and is_symbol(next_line.line_value[part.start - 1]):
                total += part.value
                continue
            # diagonal after
            if part.end < (schematic_len - 1) and is_symbol(
                next_line.line_value[part.end]
            ):
                total += part.value
                continue
            
print(total)