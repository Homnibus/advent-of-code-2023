from dataclasses import dataclass, field
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
class Gear:
    start: int
    end: int
    connected: list[Part] = field(default_factory=list)


@dataclass
class SchematicLine:
    line_number: int
    line_value: str
    parts: list[Part]
    gears: list[Gear]


def is_symbol(character: str) -> bool:
    return character not in ".0123456789"


schematic: list[SchematicLine] = []

# Input parsing
# add first empty line
schematic.append(SchematicLine(0, "." * (schematic_len + 2), [], []))
for line_index, line in enumerate(input_str.splitlines()):
    line = "." + line + "."
    current_part_list = []
    for match in re.finditer(r"[0-9]+", line):
        current_part = Part(int(match.group(0)), match.start(), match.end())
        current_part_list.append(current_part)
    current_gear_list = []
    for match in re.finditer(r"\*", line):
        current_gear = Gear(match.start(), match.end())
        current_gear_list.append(current_gear)
    current_schematic_line = SchematicLine(
        line_index + 1, line, current_part_list, current_gear_list
    )
    schematic.append(current_schematic_line)
# add last empty line
schematic.append(SchematicLine(-1, "." * (schematic_len + 2), [], []))


# Filter data
for schematic_line in schematic:
    for gear in schematic_line.gears:
        # Previous line
        previous_line = schematic[schematic_line.line_number - 1]
        for part in previous_line.parts:
            if part.start <= gear.end and part.end >= gear.start:
                gear.connected.append(part)
  
        # Current line
        for part in schematic_line.parts:
            if part.start == gear.end or part.end == gear.start:
                gear.connected.append(part)

        # Next line
        next_line = schematic[schematic_line.line_number + 1]  
        for part in next_line.parts:
            if part.start <= gear.end and part.end >= gear.start:
                gear.connected.append(part)
        
# compute total
total = 0

for schematic_line in schematic:
    for gear in schematic_line.gears:
        if len(gear.connected) == 2:
            total += gear.connected[0].value * gear.connected[1].value 

print(total)
