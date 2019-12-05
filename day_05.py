# %% Integer opcode computer
from typing import List


def get_parameters(seq, pointer, opmodes, number):
    return [seq[pointer + i + 1] if opmodes[i] else seq[seq[pointer + i + 1]] for i in range(number)]


def run_program(program_code: List[int], program_input: int) -> int:
    increments = {1: 4, 2: 4, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4}
    pointer = 0
    last_output = None
    while (opcode := program_code[pointer] % 100) != 99:
        opmodes = [program_code[pointer] // 10 ** n % 10 for n in range(2, 4)]
        if opcode == 1 or opcode == 2:
            op1, op2 = get_parameters(program_code, pointer, opmodes, 2)
            program_code[program_code[pointer + 3]] = op1 + op2 if opcode == 1 else op1 * op2
        elif opcode == 3:
            program_code[program_code[pointer + 1]] = program_input
        elif opcode == 4:
            last_output = get_parameters(program_code, pointer, opmodes, 1)[0]
        elif opcode == 5 or opcode == 6:
            op1, op2 = get_parameters(program_code, pointer, opmodes, 2)
            switch = bool(op1) if opcode == 5 else not bool(op1)
            if switch:
                pointer = op2
                continue
        elif opcode == 7 or opcode == 8:
            op1, op2 = get_parameters(program_code, pointer, opmodes, 2)
            switch = op1 < op2 if opcode == 7 else op1 == op2
            program_code[program_code[pointer + 3]] = 1 if switch else 0
        else:
            print("Unknown opcode")
        pointer += increments[opcode]
    return last_output


with open("day_05.input", "r") as input_data:
    program = [int(x) for x in input_data.readline().split(",")]

print(f"Part 1: The status code for the program is {run_program(program.copy(), 1)}")
print(f"Part 2: The status code for the program is {run_program(program.copy(), 5)}")
