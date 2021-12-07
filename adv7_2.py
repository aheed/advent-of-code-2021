import utils
from functools import cache

with utils.get_in_file() as infile:
    lines = [line for line in infile]

crabs = [int(pos) for pos in lines[0].split(",")]

print(crabs)


average = round(sum(crabs) / len(crabs))
print(average)

def calc_move_cost(origin: int, target_position: int):
    distance = abs(origin - target_position)
    cost = sum([i for i in range(distance + 1)]) #naive!!
    return cost


def calc_cost(positions: list[int], target_position: int):
    costs = [calc_move_cost(origin, target_position) for origin in positions]
    return sum(costs)


res = calc_cost(crabs, average)
print(res)

#search_window = 20
#results = [calc_cost(crabs, candidate) for candidate in range(average - search_window, average + search_window) ]
results = [calc_cost(crabs, candidate) for candidate in range(len(crabs)) ]
print(results)

min_cost = min(results)
print(min_cost)
