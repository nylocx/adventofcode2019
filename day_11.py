# %% Integer opcode computer
from __future__ import annotations
from collections import defaultdict
from itertools import tee, islice
from typing import Iterable, List
from dataclasses import dataclass
import matplotlib.pyplot as plt

import numpy as np


@dataclass
class Point:
    x: int
    y: int

    def distance_to(self, p: Point) -> int:
        return abs(p.x - self.x) + abs(p.y - self.y)

    def __iter__(self):
        yield self.y
        yield self.x

    def __add__(self, other: Point) -> Point:
        return self.__class__(self.x + other.x, self.y + other.y)

    def __hash__(self):
        return hash((self.x, self.y))


def get_parameters(seq, pointer, opmodes, number, base):
    result = []
    for i in range(number):
        if opmodes[i] == 0:
            result.append(seq[seq[pointer + i + 1]])
        elif opmodes[i] == 1:
            result.append(seq[pointer + i + 1])
        elif opmodes[i] == 2:
            result.append(seq[seq[pointer + i + 1] + base])
        else:
            print("invalid opmode")
    return result


def run_program(program_code: List[int], program_input: Iterable[int]) -> Iterable[int]:
    increments = {1: 4, 2: 4, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 2}
    input_iter = iter(program_input)
    pointer = 0
    base = 0
    while (opcode := program_code[pointer] % 100) != 99:
        opmodes = [program_code[pointer] // 10 ** n % 10 for n in range(2, 5)]
        if opcode == 1 or opcode == 2:
            op1, op2 = get_parameters(program_code, pointer, opmodes, 2, base)
            idx = program_code[pointer + 3] + (base if opmodes[2] else 0)
            program_code[idx] = op1 + op2 if opcode == 1 else op1 * op2
        elif opcode == 3:
            idx = program_code[pointer + 1] + (base if opmodes[0] else 0)
            program_code[idx] = next(input_iter)
        elif opcode == 4:
            out = get_parameters(program_code, pointer, opmodes, 1, base)[0]
            yield out
        elif opcode == 5 or opcode == 6:
            op1, op2 = get_parameters(program_code, pointer, opmodes, 2, base)
            switch = bool(op1) if opcode == 5 else not bool(op1)
            if switch:
                pointer = op2
                continue
        elif opcode == 7 or opcode == 8:
            op1, op2 = get_parameters(program_code, pointer, opmodes, 2, base)
            switch = op1 < op2 if opcode == 7 else op1 == op2
            idx = program_code[pointer + 3] + (base if opmodes[2] else 0)
            program_code[idx] = 1 if switch else 0
        elif opcode == 9:
            op = get_parameters(program_code, pointer, opmodes, 1, base)[0]
            base += op
        else:
            print("Unknown opcode")
        pointer += increments[opcode]


with open("day_11.input", "r") as input_data:
    program = defaultdict(
        int, {i: int(x) for i, x in enumerate(input_data.readline().split(","))}
    )


def run_robot(robot_program, init):
    def input_generator(region, init_value):
        yield init_value
        while True:
            yield region.get(pos, 0)

    direction = "U"
    pos = Point(0, 0)
    region_map = {}
    directions = {
        ("U", 0): "L",
        ("U", 1): "R",
        ("L", 0): "D",
        ("R", 1): "D",
        ("D", 0): "R",
        ("D", 1): "L",
        ("R", 0): "U",
        ("L", 1): "U",
    }
    delta_move = {
        "U": Point(0, -1),
        "L": Point(-1, 0),
        "D": Point(0, 1),
        "R": Point(1, 0),
    }

    a, b = tee(run_program(robot_program, input_generator(region_map, init)))
    next(b, None)
    for color, move in islice(zip(a, b), None, None, 2):
        region_map[pos] = color
        direction = directions[(direction, move)]
        pos += delta_move[direction]

    points = np.array([list(p) for p, value in region_map.items() if value])
    points -= np.min(points, axis=0)
    reg = np.zeros(np.max(points, axis=0) + 1)
    reg[points[:, 0], points[:, 1]] = 1

    return len(region_map), reg


num_paints, registration = run_robot(program.copy(), 0)
print(f"Part 1: Number of painted fields is {num_paints}")
plt.imshow(registration)
plt.show()

num_paints, registration = run_robot(program.copy(), 1)
print(f"Part 2: Number of painted fields is {num_paints}")
plt.imshow(registration)
plt.show()
