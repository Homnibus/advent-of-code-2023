from dataclasses import dataclass
from utils.api import get_input

@dataclass
class Row:
    value: str
    condition_record: list[int]

def extract_input(input_str:str) -> list[Row]:
    rows: list[Row] = []
    for line in input_str.splitlines():
        splited_lines = line.split(" ")
        value = splited_lines[0]
        condition_record = [int(value) for value in splited_lines[1].split(",")]
        rows.append(Row(value, condition_record))
    return rows
    

def is_solution_valid(input_str:str, condition_record:list[int]) -> bool:
    paded_input =  [".", *input_str, "."]
    for record in condition_record:
        if len(paded_input) == 0 or paded_input.pop(0) != ".":
            return False
        if len(paded_input) == 0:
            return False
        char = paded_input.pop(0) 
        while char != "#":
            if len(paded_input) == 0:
                return False
            char = paded_input.pop(0) 
        if char != "#":
            return False
        for i in range(record - 1):
            if len(paded_input) == 0 or paded_input.pop(0) != "#":
                return False
    for character in paded_input:
        if character != ".":
            return False
    return True

def find_arrangements(input_str:str,condition_record:list[int]) -> int:
    total = 0
    possibilities = input_str.count("?")
    for i in range(2**possibilities):
        temp_string = input_str
        binary_string = "{0:b}".format(i).rjust(possibilities,"0")
        for char in binary_string:
            if char == "0":
                temp_string=temp_string.replace("?",".",1)
            else:
                temp_string=temp_string.replace("?","#",1)
        if is_solution_valid(temp_string,condition_record):
            total += 1
    return total
    

input_str = get_input(12)
rows:list[Row] = extract_input(input_str)

total = 0
for row in rows:
    total += find_arrangements(row.value,row.condition_record)

print(total)