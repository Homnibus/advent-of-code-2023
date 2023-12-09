import re
from utils.api import get_input

def extract_values(input: list[str]) -> list[list[int]]:
    values_list: list[list[int]] = []
    for line in input:
        values_list.append([int(value) for value in re.findall(r"-?\d+", line)])
    return values_list    
    
def create_next_values(values: list[int]) -> list[int]:
    next_values: int = []
    for i in range(len(values) - 1):
        next_values.append(values[i+1] - values[i])
    return next_values

def is_full_of_zero(values: list[int]) -> bool:
    for value in values:
        if value!= 0:
            return False
    return True

def find_previous_value(values: list[int]) -> int:
    list_of_list = [values]
    current_list = values
    while not is_full_of_zero(current_list): 
        current_list = create_next_values(current_list)
        list_of_list.append(current_list)
        
    previous_value = 0
    for i in reversed(range(0,len(list_of_list)-1)):
        previous_value = list_of_list[i][0] - previous_value
    return previous_value

input_str = get_input(9)
splited_lines = input_str.splitlines()
values_list = extract_values(splited_lines)
total = 0 

for values in values_list:
   total += find_previous_value(values) 
    
print(total)