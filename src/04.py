from functools import reduce
import re
from utils.api import get_input

input_str = get_input(4)

total = 0
initial_number_of_scratchcards = 211
scratchcards_multiplier = [1]*initial_number_of_scratchcards

for line_index, line in enumerate(input_str.splitlines()):
    current_line = line.split(":")[1].split("|")
    my_numbers = re.findall(r"([0-9]+)", current_line[0])
    wining_numbers = re.findall(r"([0-9]+)", current_line[1])
    my_wining_numbers = [value for value in my_numbers if value in wining_numbers]
    total_of_win = len(my_wining_numbers)
    if total_of_win > 0:
        for i in range(line_index + 1, line_index + 1 + total_of_win):
            scratchcards_multiplier[i] += scratchcards_multiplier[line_index]
        
total = reduce(lambda x, y: x+y,scratchcards_multiplier)
        
print(total)