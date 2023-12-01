from utils.api import get_input
import regex as re

input_str = get_input(1)

def word_to_digit(word: str) -> str:
    return word.replace("one","1").replace("two","2")\
        .replace("three","3").replace("four","4").replace("five","5").replace("six","6")\
        .replace("seven","7").replace("eight","8").replace("nine","9")


total = 0
current_calibration_value = 0

for line in input_str.splitlines():
# Strugle with overlaping spelled out digits
# possible overlaping : twone, oneight, eightwo, eighthree, sevenine
# as the first 3 possible overlap make a loop, the direct replace method can't be used
    
    digits_in_line = re.findall(r"([0-9]|one|two|three|four|five|six|seven|eight|nine)", line, overlapped=True)
    first_digit = int(word_to_digit(digits_in_line[0]))
    last_digit = int(word_to_digit(digits_in_line[-1]))
    current_calibration_value = first_digit*10 + last_digit
    total += current_calibration_value
    
print(total)