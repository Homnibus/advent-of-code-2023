from __future__ import annotations
import copy
from dataclasses import dataclass
from functools import reduce
from operator import attrgetter
from utils.api import get_input


@dataclass
class Pipe:
    x: int
    y: int
    type: str
    previous_pipe: Pipe
    rotation: int = 0

    def __post_init__(self):
        if not self.previous_pipe:
            return
        if self.type == "L":
            if self.previous_pipe.x < self.x:
                self.rotation = -1
            else:
                self.rotation = +1
        elif self.type == "J":
            if self.previous_pipe.x < self.x:
                self.rotation = +1
            else:
                self.rotation = -1
        elif self.type == "7":
            if self.previous_pipe.x > self.x:
                self.rotation = -1
            else:
                self.rotation = +1
        elif self.type == "F":
            if self.previous_pipe.x > self.x:
                self.rotation = +1
            else:
                self.rotation = -1

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

    def get_inner_pipe(self, map: list[str], rotation: int) -> list[Pipe]:
        new_inner_pipes: list[Pipe] = []

        if self.type == "|":
            # comming from top
            if self.previous_pipe.x < self.x:
                inner_y = self.y - rotation
            else:
                inner_y = self.y + rotation
            if map[self.x][inner_y] == ".":
                new_inner_pipes.append(
                    Pipe(self.x, inner_y, map[self.x][inner_y], self)
                )
        elif self.type == "-":
            # comming from left
            if self.previous_pipe.y < self.y:
                inner_x = self.x + rotation
            else:
                inner_x = self.x - rotation
            if map[inner_x][self.y] == ".":
                new_inner_pipes.append(
                    Pipe(inner_x, self.y, map[inner_x][self.y], self)
                )
        elif self.type == "L":
            # comming from top
            if self.previous_pipe.x < self.x:
                if rotation > 0:
                    if map[self.x][self.y - 1] == ".":
                        new_inner_pipes.append(
                            Pipe(self.x, self.y - 1, map[self.x][self.y - 1], self)
                        )
                    if map[self.x + 1][self.y] == ".":
                        new_inner_pipes.append(
                            Pipe(self.x + 1, self.y, map[self.x + 1][self.y], self)
                        )
            else:
                if rotation < 0:
                    if map[self.x][self.y - 1] == ".":
                        new_inner_pipes.append(
                            Pipe(self.x, self.y - 1, map[self.x][self.y - 1], self)
                        )
                    if map[self.x + 1][self.y] == ".":
                        new_inner_pipes.append(
                            Pipe(self.x + 1, self.y, map[self.x + 1][self.y], self)
                        )
        elif self.type == "J":
            # comming from top
            if self.previous_pipe.x < self.x:
                if rotation < 0:
                    if map[self.x][self.y + 1] == ".":
                        new_inner_pipes.append(
                            Pipe(self.x, self.y + 1, map[self.x][self.y + 1], self)
                        )
                    if map[self.x + 1][self.y] == ".":
                        new_inner_pipes.append(
                            Pipe(self.x + 1, self.y, map[self.x + 1][self.y], self)
                        )
            else:
                if rotation > 0:
                    if map[self.x][self.y + 1] == ".":
                        new_inner_pipes.append(
                            Pipe(self.x, self.y + 1, map[self.x][self.y + 1], self)
                        )
                    if map[self.x + 1][self.y] == ".":
                        new_inner_pipes.append(
                            Pipe(self.x + 1, self.y, map[self.x + 1][self.y], self)
                        )
        elif self.type == "7":
            # comming from bottom
            if self.previous_pipe.x > self.x:
                if rotation > 0:
                    if map[self.x][self.y + 1] == ".":
                        new_inner_pipes.append(
                            Pipe(self.x, self.y + 1, map[self.x][self.y + 1], self)
                        )
                    if map[self.x - 1][self.y] == ".":
                        new_inner_pipes.append(
                            Pipe(self.x - 1, self.y, map[self.x - 1][self.y], self)
                        )
            else:
                if rotation < 0:
                    if map[self.x][self.y + 1] == ".":
                        new_inner_pipes.append(
                            Pipe(self.x, self.y + 1, map[self.x][self.y + 1], self)
                        )
                    if map[self.x - 1][self.y] == ".":
                        new_inner_pipes.append(
                            Pipe(self.x - 1, self.y, map[self.x - 1][self.y], self)
                        )
        elif self.type == "F":
            # comming from bottom
            if self.previous_pipe.x > self.x:
                if rotation < 0:
                    if map[self.x][self.y - 1] == ".":
                        new_inner_pipes.append(
                            Pipe(self.x, self.y - 1, map[self.x][self.y - 1], self)
                        )
                    if map[self.x - 1][self.y] == ".":
                        new_inner_pipes.append(
                            Pipe(self.x - 1, self.y, map[self.x - 1][self.y], self)
                        )
            else:
                if rotation > 0:
                    if map[self.x][self.y - 1] == ".":
                        new_inner_pipes.append(
                            Pipe(self.x, self.y - 1, map[self.x][self.y - 1], self)
                        )
                    if map[self.x - 1][self.y] == ".":
                        new_inner_pipes.append(
                            Pipe(self.x - 1, self.y, map[self.x - 1][self.y], self)
                        )

        return new_inner_pipes


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

starting_pipe = Pipe(75, 19, "L", None, -1)
first_pipe = Pipe(75, 20, "7", starting_pipe, 1)
visited_pipes: list[Pipe] = [starting_pipe]
to_visit_pipe = first_pipe

while to_visit_pipe != starting_pipe:
    visited_pipes.append(to_visit_pipe)
    to_visit_pipe = to_visit_pipe.get_next_pipe(padded_map)

# si negatif, on tourne en anti horaire
# si positif, on tourne en horaire
rotation = int(reduce(lambda x, y: x + y.rotation, visited_pipes, 0) / 4)

starting_pipe = Pipe(75, 19, "L", None, -1)
first_pipe = Pipe(75, 20, "7", starting_pipe, 1)
visited_pipes: list[Pipe] = [starting_pipe]
to_visit_pipe = first_pipe
inner_pipes: list[Pipe] = []

while to_visit_pipe != starting_pipe:
    for pipe in to_visit_pipe.get_inner_pipe(padded_map, rotation):
        if pipe not in inner_pipes:
            inner_pipes.append(pipe)
    visited_pipes.append(to_visit_pipe)
    to_visit_pipe = to_visit_pipe.get_next_pipe(padded_map)

print(len(inner_pipes))