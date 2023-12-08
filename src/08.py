from __future__ import annotations
from dataclasses import dataclass
from utils.api import get_input

@dataclass
class Node:
    name: str
    left: str
    right: str

def extract_direction(input: str) -> str:
    return input.splitlines()[0]

def extract_nodes(input: str) -> dict[str,Node]:
    nodes: dict[str,Node] = {}
    for line in input.splitlines()[2:]:
        name, direction = line.split(" = ")
        left, right = direction[1:-1].split(", ")
        current_node = Node(name, left, right)
        nodes[name] = current_node
    return nodes


input_str = get_input(8)
directions = extract_direction(input_str)
nodes = extract_nodes(input_str)

current_node_value = "AAA"
current_direction_index = 0
number_of_steps = 0

while current_node_value!= "ZZZ":
    if directions[current_direction_index] == "L":
        current_node_value = nodes[current_node_value].left
    else:
        current_node_value = nodes[current_node_value].right
    if current_direction_index + 1 == len(directions):
        current_direction_index = 0
    else:
        current_direction_index += 1
    number_of_steps += 1
    
print(number_of_steps)