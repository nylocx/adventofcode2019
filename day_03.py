# %% Imports
from __future__ import annotations

from dataclasses import dataclass


# %% Utils
@dataclass
class Point:
    x: int
    y: int

    def distance_to(self, p: Point) -> int:
        return abs(p.x - self.x) + abs(p.y - self.y)

    def __add__(self, other: Point) -> Point:
        return self.__class__( self.x + other.x, self.y + other.y)

    def __hash__(self):
        return hash((self.x, self.y))


#%% Better solution for Part 1 and 2
with open("day_03.input", "r") as input_data:
    wires = [l.strip().split(",") for l in input_data]

deltas = {"U": Point(0, 1), "R": Point(1, 0), "D": Point(0, -1), "L": Point(-1, 0)}
paths = []
origin = Point(0, 0)
for wire in wires:
    path = {}
    current_pos = origin
    steps = 1
    for move in wire:
        for _ in range(int(move[1:])):
            current_pos += deltas[move[0]]
            path[current_pos] = steps
            steps += 1
    paths.append(path)

xing = set.intersection(set(paths[0].keys()), set(paths[1].keys()))
print(f"Part 1: Closes distance is {min(i.distance_to(origin) for i in xing)}")
print(f"Part 2: Minimum steps are {min(paths[0][i] + paths[1][i] for i in xing)}")

