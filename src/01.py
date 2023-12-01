from utils.api import get_input
import re

input_str = get_input(1)


total = 0
current_calibration_value = 0

for line in input_str.splitlines():
    digits_in_line = re.findall(r"[0-9]",line)
    current_calibration_value = int(digits_in_line[0])*10 + int(digits_in_line[-1])
    total += current_calibration_value
    
print(total)