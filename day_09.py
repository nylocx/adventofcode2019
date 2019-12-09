# %% Integer opcode computer
from typing import Iterable, List
from itertools import permutations


def get_parameters(seq, pointer, opmodes, number, base = 0):
    result = []
    for i in range(number):
        if opmodes[i] == 0:
            result.append(seq[seq[pointer + i + 1]])
        elif opmodes[i] == 1:
            result.append(seq[pointer + i + 1])
        elif opmodes[i] == 2:
            result.append(seq[seq[pointer + i + 1] + base])
        else:
            print("Error in opmode")
    return result


def run_program(program_code: List[int], program_input: Iterable[int]) -> int:
    increments = {1: 4, 2: 4, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 2}
    input_iter = iter(program_input)
    pointer = 0
    base = 0
    while (opcode := program_code[pointer] % 100) != 99:
        opmodes = [program_code[pointer] // 10 ** n % 10 for n in range(2, 4)]
        if opcode == 1 or opcode == 2:
            op1, op2 = get_parameters(program_code, pointer, opmodes, 2, base)
            program_code[program_code[pointer + 3]] = op1 + op2 if opcode == 1 else op1 * op2
        elif opcode == 3:
            program_code[program_code[pointer + 1]] = next(input_iter)
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
            program_code[program_code[pointer + 3]] = 1 if switch else 0
        elif opcode == 9:
            print(pointer, opmodes, 1, base)
            base += get_parameters(program_code, pointer, opmodes, 1, base)[0]
        else:
            print("Unknown opcode")
        pointer += increments[opcode]


def amplifiers(program, sequence, feedback = 0):
    def amplifier_input(index):
        yield sequence[index]

        if index == 0:
            while True:
                yield feedback

        yield from run_program(program.copy(), amplifier_input(index - 1))

    for feedback in run_program(program.copy(), amplifier_input(len(sequence) - 1)):
        pass

    return feedback


with open("day_09.input", "r") as input_data:
    program = [int(x) for x in input_data.readline().split(",")] + [0] * 100000

output = next(run_program(program, [1]))

print(f"Part 1: BOOST output is {output}")
