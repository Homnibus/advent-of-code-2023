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
        return str(self.type) + self.value.replace("J", "B").replace(
            "Q", "C"
        ).replace("K", "D").replace("A", "E").replace("T", "A")

    def __post_init__(self):
        group = re.finditer(r"(\w)\1+", "".join(sorted(self.value)))

        result = [match.group(0) for match in group]
        if len(result) == 2:
            match len(result[0]):
                case 3:
                    self.type = 5
                case 2:
                    if len(result[1]) == 3:
                        self.type = 5
                    else:
                        self.type = 3
        elif len(result) == 1:
            match len(result[0]):
                case 5:
                    self.type = 7
                case 4:
                    self.type = 6
                case 3:
                    self.type = 4
                case 2:
                    self.type = 2
        else:
            self.type = 1


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
