#%%
import math
import re


def simulate(positions, velocities, steps=math.inf):
    initial_positions = positions.copy()
    initial_velocities = velocities.copy()
    step = 0
    while step < steps and (
        step == 0 or positions != initial_positions or velocities != initial_velocities
    ):
        for i in range(len(positions)):
            velocities[i] += sum(
                1 if positions[i] < position else -1
                for position in positions
                if position != positions[i]
            )
        for i in range(len(positions)):
            positions[i] += velocities[i]
        step += 1
    return step


def part1(positions):
    px, vx = [x for x, _, _ in positions], [0] * len(positions)
    py, vy = [y for _, y, _ in positions], [0] * len(positions)
    pz, vz = [z for _, _, z in positions], [0] * len(positions)
    for p, v in zip((px, py, pz), (vx, vy, vz)):
        simulate(p, v, 1000)
    return sum(
        (abs(px[i]) + abs(py[i]) + abs(pz[i])) * (abs(vx[i]) + abs(vy[i]) + abs(vz[i]))
        for i in range(len(positions))
    )


def part2(positions):
    def lcm(a, b):
        return a * b // math.gcd(a, b)

    x_repeat = simulate([x for x, _, _ in positions], [0] * len(positions))
    y_repeat = simulate([y for _, y, _ in positions], [0] * len(positions))
    z_repeat = simulate([z for _, _, z in positions], [0] * len(positions))
    return lcm(lcm(x_repeat, y_repeat), z_repeat)


with open("day_12.input") as input_data:
    positions = [list(map(int, re.findall(r"\-?\d+", l))) for l in input_data]

print(f"Part 1: Total energy is {part1(positions)}")
print(f"Part 2: State repeating after {part2(positions)} iterations")
