from dataclasses import dataclass
from operator import attrgetter
from utils.api import get_input

@dataclass
class Pipe:
    x:int
    y:int
    type: str
    distance_from_start: int
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __ne__(self, other):
        return self.x != other.x or self.y != other.y
    
    def reach_top(self) -> bool:
        return self.type in "|LJ"

    def reach_bottom(self) -> bool:
        return self.type in "|7F"

    def reach_right(self) -> bool:
        return self.type in "-LF"

    def reach_left(self) -> bool:
        return self.type in "-J7"


def add_padding(map:list[str]) -> list[str]:
    padded_map = map.copy()
    for i in range(0,len(padded_map)):
        padded_map[i] = "." + padded_map[i] + "."
    padded_map.append("." * len(map[0]))
    padded_map.insert(0,"." * len(map[0]))
    return padded_map

input_str = get_input(10)
map = input_str.splitlines()
padded_map = add_padding(map)


starting_pipe =  Pipe(75,19,"L",0)
visited_pipes: list[Pipe] = []
to_visit_pipes: list[Pipe] = [starting_pipe]

while len(to_visit_pipes) > 0:
    current_pipe = to_visit_pipes.pop(0)
    if current_pipe.reach_top():
        new_pipe = Pipe(current_pipe.x-1,current_pipe.y,padded_map[current_pipe.x-1][current_pipe.y],current_pipe.distance_from_start +1)
        if new_pipe not in visited_pipes and new_pipe not in to_visit_pipes:
            to_visit_pipes.append(new_pipe)
    if current_pipe.reach_bottom():
        new_pipe = Pipe(current_pipe.x+1,current_pipe.y,padded_map[current_pipe.x+1][current_pipe.y],current_pipe.distance_from_start +1)
        if new_pipe not in visited_pipes and new_pipe not in to_visit_pipes:
            to_visit_pipes.append(new_pipe)
    if current_pipe.reach_right():
        new_pipe = Pipe(current_pipe.x,current_pipe.y+1,padded_map[current_pipe.x][current_pipe.y+1],current_pipe.distance_from_start +1)
        if new_pipe not in visited_pipes and new_pipe not in to_visit_pipes:
            to_visit_pipes.append(new_pipe)
    if current_pipe.reach_left():
        new_pipe = Pipe(current_pipe.x,current_pipe.y-1,padded_map[current_pipe.x][current_pipe.y-1],current_pipe.distance_from_start +1)
        if new_pipe not in visited_pipes and new_pipe not in to_visit_pipes:
            to_visit_pipes.append(new_pipe)
    visited_pipes.append(current_pipe)
            
print(max(visited_pipes,key=attrgetter("distance_from_start")).distance_from_start)