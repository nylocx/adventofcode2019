# %% Imports
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass


# %% Utils
@dataclass
class Point:
    x: int
    y: int

    def distance_to(self, p: Point) -> int:
        return abs(p.x - self.x) + abs(p.y - self.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __iter__(self):
        yield self.x
        yield self.y


def add_to_grids(path_num, step_num, position):
    pos_grid[pos].add(path_num)
    if pos not in steps_grid[path_num]:
        steps_grid[path_num][position] = step_num


# %% Part 1 and Part 2
pos_grid = defaultdict(set)
steps_grid = defaultdict(dict)
origin = Point(0, 0)
with open("day_03.input", "r") as input_data:
    for i, path_line in enumerate(input_data):
        c_x, c_y = origin
        j = 1
        for step in path_line.strip().split(","):
            direction, value = step[0], int(step[1:]) + 1
            if direction == "R":
                for x in range(c_x + 1, c_x + value):
                    pos = Point(x, c_y)
                    add_to_grids(i, j, pos)
                    j += 1
                c_x = x
            elif direction == "D":
                for y in range(c_y - 1, c_y - value, -1):
                    pos = Point(c_x, y)
                    add_to_grids(i, j, pos)
                    j += 1
                c_y = y
            elif direction == "L":
                for x in range(c_x - 1, c_x - value, -1):
                    pos = Point(x, c_y)
                    add_to_grids(i, j, pos)
                    j += 1
                c_x = x
            elif direction == "U":
                for y in range(c_y + 1, c_y + value):
                    pos = Point(c_x, y)
                    add_to_grids(i, j, pos)
                    j += 1
                c_y = y
            else:
                print("Wrong input!")

pos_grid[origin] = set()
distance = None
steps = None
for point, paths in pos_grid.items():
    d = point.distance_to(origin)
    if len(paths) > 1 and (distance is None or d < distance):
        distance = d
        s = sum(steps_grid[path][point] for path in paths)
        if steps is None or s < steps:
            steps = s

print(f"Part 1: Closes distance is {distance}")
print(f"Part 2: Minimum steps are {steps}")
