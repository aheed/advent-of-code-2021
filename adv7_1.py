import utils

with utils.get_in_file() as infile:
    lines = [line for line in infile]

crabs = [int(pos) for pos in lines[0].split(",")]

def calc_move_cost(origin: int, target_position: int) -> int:
    return abs(origin - target_position)

def calc_cost(positions: list[int], target_position: int) -> int:
    costs = [calc_move_cost(origin, target_position) for origin in positions]
    return sum(costs)

results = [calc_cost(crabs, candidate) for candidate in range(len(crabs)) ]

min_cost = min(results)
print(min_cost)
