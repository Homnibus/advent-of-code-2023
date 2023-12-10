from __future__ import annotations
from dataclasses import dataclass
from operator import attrgetter
from utils.api import get_input


@dataclass
class Pipe:
    x: int
    y: int
    type: str
    previous_pipe: Pipe

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def get_next_pipe(self, map: list[str]) -> Pipe:
        next_pipe_x = self.x
        next_pipe_y = self.y

        if self.type == "|":
            if self.previous_pipe.x < self.x:
                next_pipe_x = self.x + 1
            else:
                next_pipe_x = self.x - 1
        elif self.type == "-":
            if self.previous_pipe.y < self.y:
                next_pipe_y = self.y + 1
            else:
                next_pipe_y = self.y - 1
        elif self.type == "L":
            if self.previous_pipe.x < self.x:
                next_pipe_y = self.y + 1
            else:
                next_pipe_x = self.x - 1
        elif self.type == "J":
            if self.previous_pipe.x < self.x:
                next_pipe_y = self.y - 1
            else:
                next_pipe_x = self.x - 1
        elif self.type == "7":
            if self.previous_pipe.x > self.x:
                next_pipe_y = self.y - 1
            else:
                next_pipe_x = self.x + 1
        elif self.type == "F":
            if self.previous_pipe.x > self.x:
                next_pipe_y = self.y + 1
            else:
                next_pipe_x = self.x + 1

        return Pipe(next_pipe_x, next_pipe_y, map[next_pipe_x][next_pipe_y], self)


def add_padding(map: list[str]) -> list[str]:
    padded_map = map.copy()
    for i in range(0, len(padded_map)):
        padded_map[i] = "." + padded_map[i] + "."
    padded_map.append("." * len(map[0]))
    padded_map.insert(0, "." * len(map[0]))
    return padded_map


input_str = get_input(10)
map = input_str.splitlines()
padded_map = add_padding(map)

starting_pipe = Pipe(75, 19, "L", None)
first_pipe = Pipe(75, 20, "7", starting_pipe)
visited_pipes: list[Pipe] = [starting_pipe]
to_visit_pipe = first_pipe

while to_visit_pipe != starting_pipe:
    visited_pipes.append(to_visit_pipe)
    to_visit_pipe = to_visit_pipe.get_next_pipe(padded_map)

print(int(len(visited_pipes) / 2))
