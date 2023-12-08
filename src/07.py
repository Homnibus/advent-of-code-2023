from utils.api import get_input
from dataclasses import dataclass
from operator import attrgetter
import re


@dataclass
class Hand:
    value: str
    bid: int
    type: int = 0

    @property
    def sorting_value(self) -> str:
        return str(self.type) + self.value.replace("J", "0").replace(
            "Q", "C"
        ).replace("K", "D").replace("A", "E").replace("T", "A")

    def __post_init__(self):
        striped_value = self.value.replace("J","")
        number_of_j = 5 - len(striped_value)
        group = re.finditer(r"(\w)\1+", "".join(sorted(striped_value)))
        type_list = [1,2,4,6,7,7]

        result = [match.group(0) for match in group]
        if len(result) == 2:
            if len(result[0]) == len(result[1]) and number_of_j == 0:
                self.type = 3
            else : 
                self.type = 5
        else:
            if len(result) == 1:
                nomber_of_consecutive_letters = len(result[0])
            else:
                 nomber_of_consecutive_letters = 1
            self.type = type_list[nomber_of_consecutive_letters - 1 + number_of_j]     

def extract_hands(input: str) -> list[Hand]:
    hands: list[Hand] = []
    for line in input.splitlines():
        values_str = re.findall(r"\w+", line)
        hands.append(Hand(values_str[0], int(values_str[1])))
    return hands


input_str = get_input(7)
hands: list[Hand] = extract_hands(input_str)
sorted_hands = sorted(hands, key=attrgetter("sorting_value"))
total = 0

for index, hand in enumerate(sorted_hands):
    total += (index + 1) * hand.bid

print(total)
