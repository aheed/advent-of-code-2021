#from typing import Type
from __future__ import annotations
from dataclasses import dataclass
from sys import version
from typing import Literal
import utils


with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

message = lines[0]
print(message)

print(int(message[0], 16))
print(f"{bin(int(message[2], 16)).split('0b')[1]}")
print(f"{int(message[2], 16):04b}")



messages_bin = [f"{int(hex_char, 16):04b}" for hex_char in message]
message_bin = ""
for mess in messages_bin:
    message_bin += mess
#print(messages_bin)
#print(message_bin)

@dataclass(frozen=True)
class Packet:
    version: int
    packet_type: int
    Literal: int
    #length_type: int
    #length: int
    subpackets: list[Packet]

#a = Packet(1, [Packet(2, [])])

def bin_to_int(number: str, length: int) -> int:
    bits = [int(bit) for bit in number[:length]]
    res = int(0)
    for bit in bits:
        res <<= 1
        res += bit
    return res

def bin_to_version(ver: str) -> int:
    return bin_to_int(ver, 3)

def bin_to_packet_type(t: str) -> int:
    return bin_to_int(t, 3)

def bin_to_literal(l: str) -> int:
    nof_nibbles = int(0)
    bin_literal = ""
    done = False
    while not done:                
        bin_literal += l[nof_nibbles * 5 + 1:(nof_nibbles*5) + 5]
        done = l[nof_nibbles * 5] == "0"
        nof_nibbles += 1

    print(l)
    print(bin_literal)
    print(nof_nibbles * 4)
    return bin_to_int(bin_literal, nof_nibbles * 4)

t = bin_to_version(message_bin)
print(t)
print(bin_to_version("1011010101"))
print(bin_to_packet_type("1011010101"))

def bin_to_packet(bin: str) -> Packet:
    version = bin_to_packet_type(bin)
    packet_type = bin_to_packet_type(bin[3:])

    literal_val = 0
    subpackets: list[Packet] = []
    
    if packet_type == 4:
        literal_val = bin_to_literal(bin[6:])

    if packet_type != 4:
        pass #todo: read subpackets

    return Packet(version, packet_type, literal_val, subpackets)

#p = bin_to_packet(message_bin)
#print(p)

pp = bin_to_packet("110100101111111000101000")
print(pp)