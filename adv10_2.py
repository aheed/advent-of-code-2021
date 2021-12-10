from dataclasses import dataclass
import utils


with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]


def is_opening_bracket(character: str) -> bool:
    return character == "(" or character == "[" or character == "<" or character == "{"

def get_closing_bracket(opening_character: str) -> str:
    if (opening_character == "("):
        return ")"
    if (opening_character == "["):
        return "]"
    if (opening_character == "<"):
        return ">"
    if (opening_character == "{"):
        return "}"
    raise Exception("should not happen")    

def get_closing_sequence(line: str) -> str:
    stack: list[str] = []

    for character in line:
        if (is_opening_bracket(character)):
            stack.append(character)
        
        elif len(stack) == 0 or character != get_closing_bracket(stack[-1]):
            return "illegal"

        else:
            stack.pop()

    stack.reverse()
    return "".join([get_closing_bracket(ch) for ch in stack])

closing_sequences = [get_closing_sequence(line) for line in lines]

def get_outcomplete_score(character: str) -> int:
    if (character == ")"):
        return 1
    if (character == "]"):
        return 2
    if (character == "}"):
        return 3
    if (character == ">"):
        return 4
    return 0

def calc_closing_sequence_score(seq: str) -> int:
    total: int = 0
    for character in seq:
        total *= 5
        total += get_outcomplete_score(character)
    return total

closing_sequences_scores = [calc_closing_sequence_score(seq) for seq in closing_sequences if seq != "illegal"]
closing_sequences_scores.sort()
middle_index = int((len(closing_sequences_scores)) / 2)
print(closing_sequences_scores[middle_index])
