from __future__ import annotations
from dataclasses import dataclass
import utils

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

@dataclass
class Instruction:
    on: bool
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    z_min: int
    z_max: int

size = 50

def read_bounds(inp: str) -> tuple[int, int]:
    min_val, max_val = inp[2:].split("..")
    return (int(min_val) + size, int(max_val) + size)

def read_instruction(inp: str) -> Instruction:
    on = inp[:2] == "on"
    all_bounds = inp.split(" ")[1].split(",")
    x_min, x_max = read_bounds(all_bounds[0])
    y_min, y_max = read_bounds(all_bounds[1])
    z_min, z_max = read_bounds(all_bounds[2])
    return Instruction(on, x_min, x_max, y_min, y_max, z_min, z_max)

all_instructions = [read_instruction(line) for line in lines]

print(all_instructions[9:11])


cubes = [[[int(0)] * 2 * size for _ in range(2 * size)] for _ in range(2 * size)]


def is_in_bounds(x: int, y: int, z: int) -> bool:
    return x >= 0 and x < (2*size) and y >= 0 and y < (2*size) and z >= 0 and z < (2*size)

for i, instr in enumerate(all_instructions[:20]):
    print(i)
    for x in range(instr.x_min, instr.x_max + 1):
        for y in range(instr.y_min, instr.y_max + 1):
            for z in range(instr.z_min, instr.z_max + 1):
                if is_in_bounds(x, y, z):
                    cubes[x][y][z] = int(1) if instr.on else int(0)

total_lit = int(0)
for x in range(0, 2 * size):
    for y in range(0, 2 * size):
        for z in range(0, 2 * size):
            total_lit += cubes[x][y][z]

print(total_lit)




