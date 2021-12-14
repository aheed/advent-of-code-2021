import utils

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

template = lines[0]

rules: dict[str, str] = {}

for line in lines[2:]:
    parts = line.split(" -> ")
    rules[parts[0]] = parts[1]

#print(template)
#print(rules)

def step(in_polymer: str) -> str:
    out_polymer = ""
    in_len = len(in_polymer)
    for i in range(in_len):
        out_polymer += in_polymer[i]
        if i < (in_len - 1):
            key = f"{in_polymer[i]}{in_polymer[i + 1]}"
            if key in rules:
                out_polymer += rules[key]
    return out_polymer

#p1 = step(template)
#print(p1)

end_polymer = template

for i in range(10):
    end_polymer = step(end_polymer)

#print(end_polymer)
print(len(end_polymer))

all_chars = set(end_polymer)
print(all_chars)

def get_quantity(character: str) -> int:
    return len([c for c in end_polymer if c == character])

quantities = [get_quantity(character) for character in all_chars]
quantities.sort(reverse=True)
print(quantities)
res = quantities[0] - quantities[-1]
print(res)
