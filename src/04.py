import re
from utils.api import get_input

input_str = get_input(4)

total = 0

for line in input_str.splitlines():
    current_line = line.split(":")[1].split("|")
    my_numbers = re.findall(r"([0-9]+)", current_line[0])
    wining_numbers = re.findall(r"([0-9]+)", current_line[1])
    my_wining_numbers = [value for value in my_numbers if value in wining_numbers]
    total_of_win = len(my_wining_numbers)
    if total_of_win > 0:
        total += pow(2, total_of_win-1)

print(total)