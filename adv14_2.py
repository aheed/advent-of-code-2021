from functools import cache
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

def merge_histograms(h1: dict[str, int], h2: dict[str, int]) -> dict[str, int]:
    res: dict[str, int] = {}
    for key, val in h1.items():
        res[key] = val
    for key, val in h2.items():
        if key in h1:
            res[key] = h1[key] + val
        else:
            res[key] = val
    return res

# returns occurrences of each character after a given number of iterations
@cache
def calc_histogram(polymer: str, iterations: int) -> dict[str, int]:

    if len(polymer) == 1:
        return {polymer: 1}

    if len(polymer) > 2:
        part1 = calc_histogram(polymer[:2], iterations)
        part2 = calc_histogram(polymer[1:], iterations)
        res = merge_histograms(part1, part2)
        res[polymer[1]] -= 1
        return res

    if iterations <= 0 or polymer not in rules:
        return merge_histograms({polymer[0] : 1}, {polymer[1] : 1})
    
    subpair1 = polymer[0] + rules[polymer]
    subhist1 = calc_histogram(subpair1, iterations - 1)

    subpair2 = rules[polymer] + polymer[1]
    subhist2 = calc_histogram(subpair2, iterations - 1)

    res = merge_histograms(subhist1, subhist2)
    res[rules[polymer]] -= 1
    return res

total_iterations = 40
end_histogram = calc_histogram(template, total_iterations)
#print(end_histogram)

#print(end_histogram.values())
quantities = [val for val in end_histogram.values()]
quantities.sort(reverse=True)
#print(quantities)

res = quantities[0] - quantities[-1]
print(res)