# %%
from __future__ import annotations
from dataclasses import dataclass
from itertools import combinations
import re

@dataclass
class Point:
    x: int = 0
    y: int = 0
    z: int = 0

    @classmethod
    def from_text(cls, text: str) -> Point:
        return cls(*[int(x) for x in re.findall(r"\-?\d+", text)])

    def gravity(self, other):
        return self.__class__(*(-1 if a > b else (1 if b > a else 0) for a, b in zip(self, other)))

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __neg__(self):
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z
        return self

    def __abs__(self):
        return self.__class__(*[abs(x) for x in self])

    def __add__(self, other: Point) -> Point:
        return self.__class__(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return self + -other

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __isub__(self, other):
        self += -other
        return self

    def __hash__(self):
        return hash((self.x, self.y, self.z))


with open("day_12.input", "r") as input_data:
    positions = [Point.from_text(l.strip()) for l in input_data]

initial_positions = positions.copy()
velocities = [Point() for _ in positions]
pairs = list(combinations(range(len(positions)), 2))

for _ in range(1000):
    for a, b in pairs:
        gravity = positions[a].gravity(positions[b])
        velocities[a] += gravity
        velocities[b] -= gravity

    for p, v in zip(positions, velocities):
        p += v

pot_energy = [sum(abs(p)) for p in positions]
kin_energy = [sum(abs(v)) for v in velocities]
sum_total_energy = sum(p * k for p, k in zip(pot_energy, kin_energy))
print(f"Part 1: Total energy after {_ + 1} iterations is {sum_total_energy}")
