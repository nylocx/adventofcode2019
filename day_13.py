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
        yield self.x
        yield self.y

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


with open("day_13.input", "r") as input_data:
    program = defaultdict(
        int, {i: int(x) for i, x in enumerate(input_data.readline().split(","))}
    )


def run_arcade(arcade_program):
    a, b, c = tee(run_program(arcade_program, [0]), 3)
    next(b, None)
    next(c, None)
    next(c, None)
    tile_map = {}
    for x, y, tile_id in islice(zip(a, b, c), None, None, 3):
        tile_map[(Point(x, y))] = tile_id

    return tile_map

tile_map = run_arcade(program.copy())
print(f"Part 1: Number of tiles {len([x for x in tile_map.values() if x == 2])}")
program[0] = 2
tile_map = run_arcade(program.copy())

