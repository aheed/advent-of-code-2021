from __future__ import annotations
from dataclasses import dataclass
import math

import utils


def hex_to_bin(hex_mess: str) -> str:
    messages_bin = [f"{int(hex_char, 16):04b}" for hex_char in hex_mess]
    message_bin = ""
    for mess in messages_bin:
        message_bin += mess
    return message_bin

@dataclass(frozen=True)
class Packet:
    version: int
    packet_type: int
    literal_val: int
    subpackets: list[Packet]

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

    length = nof_nibbles * 5

    return (length, bin_to_int(bin_literal, nof_nibbles * 4))

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

def evaluate_packet(packet: Packet) -> int:
    if packet.packet_type == 4:
        return packet.literal_val

    if packet.packet_type == 0:
        return sum([evaluate_packet(subpacket) for subpacket in packet.subpackets])

    if packet.packet_type == 1:
        return math.prod([evaluate_packet(subpacket) for subpacket in packet.subpackets])

    if packet.packet_type == 2:
        return min([evaluate_packet(subpacket) for subpacket in packet.subpackets])

    if packet.packet_type == 3:
        return max([evaluate_packet(subpacket) for subpacket in packet.subpackets])

    if packet.packet_type == 5:
        assert(len(packet.subpackets) == 2)
        return int(evaluate_packet(packet.subpackets[0]) > evaluate_packet(packet.subpackets[1]))
    
    if packet.packet_type == 6:
        assert(len(packet.subpackets) == 2)
        return int(evaluate_packet(packet.subpackets[0]) < evaluate_packet(packet.subpackets[1]))

    if packet.packet_type == 7:
        assert(len(packet.subpackets) == 2)
        return int(evaluate_packet(packet.subpackets[0]) == evaluate_packet(packet.subpackets[1]))

    raise Exception("unexpected packet type")

###################################

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

message = lines[0]
message_bin = hex_to_bin(message)

(top_packet_length, top_packet) = bin_to_packet(message_bin)

res =  evaluate_packet(top_packet)
print(res)

