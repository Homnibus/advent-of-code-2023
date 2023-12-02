from __future__ import annotations
from functools import reduce
from utils.api import get_input
from dataclasses import dataclass, field
import regex as re

input_str = get_input(2)

class SetOfCube:
    red: int
    green: int
    blue: int
    
    def __init__(self,set_record=""):
        color_count = re.findall(r"[0-9]+\sred", set_record)
        if len(color_count) > 0:
            self.red = int(color_count[0][:-4])
        else:
            self.red = 0
            
        color_count = re.findall(r"[0-9]+\sgreen", set_record)
        if len(color_count) > 0:
            self.green = int(color_count[0][:-6])
        else:
            self.green = 0    
            
        color_count = re.findall(r"[0-9]+\sblue", set_record)
        if len(color_count) > 0:
            self.blue = int(color_count[0][:-5])
        else:
            self.blue = 0

    def is_lower(self, control_set: SetOfCube) -> bool:
        if self.red > control_set.red:
            return False
        if self.green > control_set.green:
            return False
        if self.blue > control_set.blue:
            return False
        return True

@dataclass
class Game:
    id: int
    sets: list[SetOfCube] = field(default_factory=list)
    
    def is_possible(self, control_set: SetOfCube):
        return len(list(filter(lambda set: set.is_lower(control_set) ,self.sets))) == len(self.sets)
    
# Init data structures    
game_list: list[Game] = []

for line in input_str.splitlines():
    game_number_splited_line = line.split(":")
    game_number = int(game_number_splited_line[0][5:])
    set_list = game_number_splited_line[1].split(";")
    
    current_game = Game(game_number)

    for set_record in set_list:
        current_set = SetOfCube(set_record)
        current_game.sets.append(current_set)
    
    game_list.append(current_game)
    
# Filter data structures
max_set = SetOfCube()
max_set.red = 12
max_set.green = 13
max_set.blue = 14

possible_games = list(filter(lambda game: game.is_possible(max_set),game_list))

sum_of_id_of_possible_games = reduce(lambda x, y: x+y,list(map(lambda game: game.id,possible_games)))

print(sum_of_id_of_possible_games)