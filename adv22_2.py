from __future__ import annotations
from dataclasses import dataclass
import utils

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

@dataclass
class Instruction:
    _on: bool
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    z_min: int
    z_max: int

    @property
    def on(self) -> bool:
        return self._on

    @on.setter
    def on(self, v: bool) -> None:
        self._on = v

def read_bounds(inp: str) -> tuple[int, int]:
    min_val, max_val = inp[2:].split("..")
    return (int(min_val), int(max_val))

def read_instruction(inp: str) -> Instruction:
    on = inp[:2] == "on"
    all_bounds = inp.split(" ")[1].split(",")
    x_min, x_max = read_bounds(all_bounds[0])
    y_min, y_max = read_bounds(all_bounds[1])
    z_min, z_max = read_bounds(all_bounds[2])
    return Instruction(on, x_min, x_max, y_min, y_max, z_min, z_max)

all_instructions = [read_instruction(line) for line in lines]

#print(all_instructions[9:11])


#cubes = [[[int(0)] * 2 * size for _ in range(2 * size)] for _ in range(2 * size)]

# def is_in_bounds(x: int, y: int, z: int) -> bool:
#     return x >= 0 and x < (2*size) and y >= 0 and y < (2*size) and z >= 0 and z < (2*size)

# for i, instr in enumerate(all_instructions[:20]):
#     print(i)
#     for x in range(instr.x_min, instr.x_max + 1):
#         for y in range(instr.y_min, instr.y_max + 1):
#             for z in range(instr.z_min, instr.z_max + 1):
#                 if is_in_bounds(x, y, z):
#                     cubes[x][y][z] = int(1) if instr.on else int(0)

# total_lit = int(0)
# for x in range(0, 2 * size):
#     for y in range(0, 2 * size):
#         for z in range(0, 2 * size):
#             total_lit += cubes[x][y][z]

# print(total_lit)

def overlap(i1: Instruction, i2: Instruction, on: bool) -> Instruction | None:
    x_min = max(i1.x_min, i2.x_min)
    x_max = min(i1.x_max, i2.x_max)
    y_min = max(i1.y_min, i2.y_min)
    y_max = min(i1.y_max, i2.y_max)
    z_min = max(i1.z_min, i2.z_min)
    z_max = min(i1.z_max, i2.z_max)
    if x_min <= x_max and y_min <= y_max and z_min <= z_max:
        return Instruction(on, x_min, x_max, y_min, y_max, z_min, z_max)


def get_count(ins: Instruction) -> int:
    return (ins.x_max + 1 - ins.x_min) * (ins.y_max + 1 - ins.y_min) * (ins.z_max + 1 - ins.z_min) * (1 if ins.on else -1)


layers: list[Instruction] = []

r1 = int(0)
#for i, instruction in enumerate(all_instructions[:20]):
for i, instruction in enumerate(all_instructions):
    print(i)
    new_layers: list[Instruction] = []
    for layer in layers:
        ol = overlap(layer, instruction,  not layer.on)
        if not ol is None:
            new_layers.append(ol)
    if instruction.on:
        new_layers.append(instruction)
    r_new = sum((get_count(l) for l in new_layers))
    r1 += r_new
    print(instruction.on, r_new, r1, len(new_layers))
    layers += new_layers

print(len(layers))



res = sum((get_count(layer) for layer in layers))
print(res)

# res = int(0)
# for i, layer in enumerate(layers):
#     print(i)
#     res += layer.

# 202115663174176 is too low

