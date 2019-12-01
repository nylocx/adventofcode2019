#%% Compute the fuel usage given the formula (Part 1)
with open("day_01.input", "r") as input_data:
    print(f"Part 1: The needed fuel is: {sum(int(x) // 3 - 2 for x in input_data)}")


#%% Compute the fuel taking into account that fuel itself adds mass (Part 2)
def compute_fuel(mass):
    return 0 if (fuel:= mass // 3 - 2) <= 0 else fuel + compute_fuel(fuel)


with open("day_01.input", "r") as input_data:
    print(f"Part 2: The needed fuel is: {sum(compute_fuel(int(x)) for x in input_data)}")
