from dataclasses import dataclass
import utils


with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

stack: list[str] = []

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
    
def get_error_score(closing_character: str) -> int:
    if (closing_character == ")"):
        return 3
    if (closing_character == "]"):
        return 57
    if (closing_character == "}"):
        return 1197
    if (closing_character == ">"):
        return 25137
    
    return 0

def get_illegal_char(line: str) -> str:
    for character in line:
        if (is_opening_bracket(character)):
            stack.append(character)
        
        elif len(stack) == 0 or character != get_closing_bracket(stack[-1]):
            return character

        else:
            stack.pop()

    return "-"

#print(get_illegal_char(lines[0]))

result_chars = [get_illegal_char(line) for line in lines]
print(result_chars)
score = sum([get_error_score(get_illegal_char(line)) for line in lines])
print(score)