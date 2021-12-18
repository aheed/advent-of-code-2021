from functools import cache
import utils


with utils.get_in_file() as infile:
    lines = [line for line in infile]

grid: list[list[int]] = [[int(depth) for depth in list(line.strip())] for line in lines]
size = len(grid[0])


def is_in_bounds(row: int, col: int) -> bool:
    return row >= 0 and row < size and col >= 0 and col < size

def get_neighbors(row: int, col: int) -> list[list[int]]:
    neigh: list[list[int]] = []

    def add_if_in_bounds(row: int, col: int):
        if is_in_bounds(row, col):
            neigh.append([row, col])
    
    add_if_in_bounds(row - 1, col)
    add_if_in_bounds(row + 1, col)
    add_if_in_bounds(row, col - 1)
    add_if_in_bounds(row, col + 1)    
    return neigh

res_cached: list[list[int]] = [[False] * size for _ in range(size)]
res_cache: list[list[int]] = [[1000000] * size for _ in range(size)]
res_cached_values = int(0)

@cache
def calc_min_risk(start_row: int, start_col: int, start_risk: int, start_max_risk: int) -> int:

    global res_cache
    global res_cached
    global res_cached_values

    if res_cached[start_row][start_col]:
        return start_risk + res_cache[start_row][start_col]

    node_risk = grid[start_row][start_col]
    min_risk = start_risk + node_risk

    if min_risk > start_max_risk:
        return min_risk
    
    if start_row == 0 and start_col == 0:
        return start_risk

    neighbors = get_neighbors(start_row, start_col)
    best_candidate = start_max_risk
    for neigbor in neighbors:
        candidate = calc_min_risk(neigbor[0], neigbor[1], min_risk, best_candidate)
        if candidate < best_candidate:
            best_candidate = candidate

    #if best_candidate >= start_max_risk:
    #    raise Exception(f"should not happen {start_row} {start_col} {best_candidate}")

    if best_candidate < start_max_risk:
        
        res_cache[start_row][start_col] = best_candidate - start_risk
        res_cached[start_row][start_col] = True
        res_cached_values += 1
        print(f"got a result {res_cached_values}")
    return best_candidate
    

#res = calc_total_risk_on_entry(0, 0) - grid[0][0]
#max_result = int(size * 2 * 9)
max_result = int(400)
#res = calc_min_risk(9, 9, 0, max_result)
res = calc_min_risk(size - 1, size - 1, 0, max_result)
print(res)


    