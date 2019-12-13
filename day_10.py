# %% Day 10
import numpy as np


def normalized(vector):
    a, b = sorted(np.abs(vector))
    if a == b == 0:
        return tuple(vector)
    if a == 0:
        return tuple(vector // b)

    while a := a % b:
        a, b = b, a

    return tuple(vector // b)


with open("day_10.input", "r") as input_data:
    asteroid_map = np.array(
        [[0 if c == "." else 1 for c in x.strip()] for x in input_data], dtype=int
    )

asteroids = np.stack(np.nonzero(asteroid_map), axis=1)
max_viewable = 0
station = (0, 0)
for asteroid in asteroids:
    viewable = len({normalized(x - asteroid) for x in asteroids}) - 1
    if viewable > max_viewable:
        max_viewable = viewable
        station = asteroid

print(f"Part 1: The station asteroid is {station} with {max_viewable} observables")

directions = {normalized(x - station) for x in asteroids}
directions.remove((0, 0))
d = sorted(directions, key=lambda x: np.mod(np.arctan2(x[1], -x[0]), 2 * np.pi))[199]
k = 1
while not asteroid_map[station[0] + d[0] * k, station[1] + d[1] * k]:
    k += 1

print(
    f"Part 2: 200 destroyed asteroid is {station[0] + d[0] * k, station[1] + d[1] * k}")
