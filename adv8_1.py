from dataclasses import dataclass
import utils


with utils.get_in_file() as infile:
    lines = [line for line in infile]

# @dataclass
# class SegmentCombo:
#     segments: list[str]

@dataclass
class Entry:
    digits: list[list[str]]
    output: list[list[str]]

def create_entry(instring: str) -> Entry:
    parts = instring.strip().split(" | ")
    digit_strings = parts[0].split(" ")
    digits = [list(charac) for charac in digit_strings]
    output_strings = parts[1].split(" ")
    output = [list(charac) for charac in output_strings]
    return Entry(digits, output)


entries = [create_entry(line) for line in lines]

def criterion(segment_combo: list[str]) -> bool:
    l = len(segment_combo)
    return l == 2 or l == 3 or l == 4 or l == 7

def occurrences(entry: Entry) -> int:
    return len([segment for segment in entry.output if criterion(segment)])

all_occurences = [occurrences(entry) for entry in entries]
print(sum(all_occurences))