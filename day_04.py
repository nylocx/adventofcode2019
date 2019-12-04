#%% Solution Day 4
lower = 356261
upper = 846303

counter1 = 0
counter2 = 0

while lower < upper:
    low = str(lower)
    digits = [-1] + [int(x) for x in low] + [-1]
    valid1 = False
    valid2 = False

    for k, (a, b, c, d) in enumerate(zip(
        digits[1:-2], digits[2:-1], digits[:-3], digits[3:]
    )):
        if a > b:
            valid1 = valid2 = False
            lower = int("".join(x if i < k else low[k] for i, x in enumerate(low))) - 1
            break
        valid1 |= a == b
        valid2 |= a == b and a != c and b != d
    lower += 1
    counter1 += valid1
    counter2 += valid2

print(f"Part 1: {counter1} possible passwords")
print(f"Part 2: {counter2} possible passwords")
