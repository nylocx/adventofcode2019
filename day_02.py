# %% Integer optcode computer (Part 1)
with open("day_02.input", "r") as input_data:
    sequence = [int(x) for x in input_data.readline().split(",")]
    sequence[1] = 12
    sequence[2] = 2
    for i in range(0, len(sequence), 4):
        value = sequence[i]
        if value == 99:
            print(f"Part 1: Result {sequence[0]}")
            break
        op1 = sequence[sequence[i + 1]]
        op2 = sequence[sequence[i + 2]]
        target_index = sequence[i + 3]
        sequence[target_index] = op1 + op2 if value == 1 else op1 * op2

# %% Integer optcode computer (Part 2)
with open("day_02.input", "r") as input_data:
    sequence = [int(x) for x in input_data.readline().split(",")]
for noun in range(100):
    for verb in range(100):
        current_sequence = sequence.copy()
        current_sequence[1] = noun
        current_sequence[2] = verb
        for i in range(0, len(current_sequence), 4):
            value = current_sequence[i]
            if value == 99:
                if current_sequence[0] == 19690720:
                    print(f"Part 2: Result {100 * noun + verb}")
                break
            op1 = current_sequence[current_sequence[i + 1]]
            op2 = current_sequence[current_sequence[i + 2]]
            target_index = current_sequence[i + 3]
            current_sequence[target_index] = op1 + op2 if value == 1 else op1 * op2
