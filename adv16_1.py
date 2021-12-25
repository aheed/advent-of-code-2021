#from typing import Type
from __future__ import annotations
from dataclasses import dataclass

import utils


with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

message = lines[0]
print(message)

print(int(message[0], 16))
print(f"{bin(int(message[2], 16)).split('0b')[1]}")
print(f"{int(message[2], 16):04b}")

def hex_to_bin(hex_mess: str) -> str:
    messages_bin = [f"{int(hex_char, 16):04b}" for hex_char in hex_mess]
    message_bin = ""
    for mess in messages_bin:
        message_bin += mess
    return message_bin    

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

def bin_to_literal(l: str) -> tuple[int, int]:
    nof_nibbles = int(0)
    bin_literal = ""
    done = False
    while not done:                
        bin_literal += l[nof_nibbles * 5 + 1:(nof_nibbles*5) + 5]
        done = l[nof_nibbles * 5] == "0"
        nof_nibbles += 1

    #nof_input_nibbles = (nof_nibbles * 5 + 3) // 4
    #length = nof_input_nibbles * 4
    length = nof_nibbles * 5

    print(l)
    print(bin_literal)
    print(length)
    
    return (length, bin_to_int(bin_literal, nof_nibbles * 4))

t = bin_to_version(message_bin)
print(t)
print(bin_to_version("1011010101"))
print(bin_to_packet_type("1011010101"))

def bin_to_packet(bin: str) -> tuple[int, Packet]:
    version = bin_to_packet_type(bin)
    packet_type = bin_to_packet_type(bin[3:])

    literal_val = int(0)
    subpackets: list[Packet] = []
    length = int(6)
    remainder = bin[length:]
    
    if packet_type == 4:
        (literal_length, literal_val) = bin_to_literal(remainder)
        length += literal_length

    else:
        
        if remainder[0] == "0":
            #15-bit bit count format
            remainder = remainder[1:]
            length += 1
            subpackets_length = bin_to_int(remainder, 15)
            length += 15
            remainder = remainder[15:]
            subpackets_length_read = int(0)

            while subpackets_length_read < subpackets_length:
                (subpacket_length, subpacket) = bin_to_packet(remainder)
                subpackets.append(subpacket)
                subpackets_length_read += subpacket_length
                remainder = remainder[subpacket_length:]
            length += subpackets_length_read
        else:
            #11-bit subpacket count format
            remainder = remainder[1:]
            length += 1
            nof_subpackets = bin_to_int(remainder, 11)
            length += 11
            remainder = remainder[11:]
            nof_subpackets_read = int(0)

            while nof_subpackets_read < nof_subpackets:
                (subpacket_length, subpacket) = bin_to_packet(remainder)
                subpackets.append(subpacket)
                nof_subpackets_read += 1
                remainder = remainder[subpacket_length:]
                length += subpacket_length

    return (length, Packet(version, packet_type, literal_val, subpackets))

#p = bin_to_packet(message_bin)
#print(p)

#pp = bin_to_packet("110100101111111000101000")
#pp = bin_to_packet("00111000000000000110111101000101001010010001001000000000")
#(ll, pp) = bin_to_packet("11101110000000001101010000001100100000100011000001100000")
#print(ll)
#print(pp)

def sum_versions(packet: Packet) -> int:
    subpackets_sum = sum([sum_versions(subpacket) for subpacket in packet.subpackets])
    return packet.version + subpackets_sum

#print(sum_versions(pp))

# (ex1_l, ex1_p) = bin_to_packet(hex_to_bin("8A004A801A8002F478"))
# print(ex1_l)
# print(ex1_p)
# print(sum_versions(ex1_p))

# (ex1_l, ex1_p) = bin_to_packet(hex_to_bin("620080001611562C8802118E34"))
# print(ex1_l)
# print(ex1_p)
# print(sum_versions(ex1_p))

(ex1_l, ex1_p) = bin_to_packet(hex_to_bin("C0015000016115A2E0802F182340"))
print(ex1_l)
print(ex1_p)
print(sum_versions(ex1_p))

(top_packet_length, top_packet) = bin_to_packet(message_bin)
print(sum_versions(top_packet))