from __future__ import annotations
from dataclasses import dataclass
import math
import utils

@dataclass
class SnailLiteral:
    value: int
    depth: int

@dataclass
class SnailNumber:
    seq: list[SnailLiteral]

def read(line: str) -> SnailNumber:
    seq: list[SnailLiteral] = []
    depth = int(0)
    for character in line:
        if character == "[":
            depth += 1
        elif character == "]":
            depth -= 1
        elif character == ",":
            pass
        else:
            seq.append(SnailLiteral(int(character), depth))
    return SnailNumber(seq)


def explode(n: SnailNumber, index: int) -> SnailNumber:
    if index > 0:
        n.seq[index - 1] = SnailLiteral(n.seq[index - 1].value + n.seq[index].value, n.seq[index - 1].depth)
    
    if index < (len(n.seq) - 2):
        n.seq[index + 2] = SnailLiteral(n.seq[index + 2].value + n.seq[index + 1].value, n.seq[index + 2].depth)
    
    n.seq.pop(index + 1)
    n.seq[index] = SnailLiteral(0, n.seq[index].depth - 1)
    return n

def split(n: SnailNumber, index: int) -> SnailNumber:
    left_val = n.seq[index].value // 2
    right_val = math.ceil(n.seq[index].value / 2)
    new_depth = n.seq[index].depth + 1
    n.seq[index] = SnailLiteral(right_val, new_depth)
    n.seq.insert(index, SnailLiteral(left_val, new_depth))
    return n

def reduce(n: SnailNumber) -> SnailNumber:
    #return n #TEMP!!!
    res = n
    while True:
        explode_index = next((index for index, lit in enumerate(res.seq) if lit.depth == 4), None)
        if not explode_index is None:
            res = explode(res, explode_index)
        else:
            split_index = next((index for index, lit in enumerate(res.seq) if lit.value >= 10), None)
            if split_index is None:
                break
            res = split(res, split_index)
    return res

def add(n1: SnailNumber, n2: SnailNumber) -> SnailNumber:
    unreduced = SnailNumber([SnailLiteral(l.value, l.depth + 1) for l in n1.seq + n2.seq])
    reduced = reduce(unreduced)
    return reduced

def magnitude(n: SnailNumber) -> int:
    depth = 4 #assume there is no greater depth in n

    while True:
        index = next((index for index, lit in enumerate(n.seq) if lit.depth == depth), None)
        if index is None:
            depth -= 1
            if depth == 0:
                assert(len(n.seq) == 1)
                return n.seq[0].value
        else:
            v = n.seq[index].value * 3 + n.seq[index + 1].value * 2
            n.seq[index] = SnailLiteral(v, depth - 1)
            n.seq.pop(index + 1)

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

#print(read(lines[0]))
r = add(read(lines[0]), read(lines[1]))
print(r)
#print(magnitude(r))

#n = read("[9,1]")
n = read("[[9,1],[1,9]]")
print("\n")
print(n)
print(magnitude(n))
