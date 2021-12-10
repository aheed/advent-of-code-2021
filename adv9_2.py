from dataclasses import dataclass
import utils


with utils.get_in_file() as infile:
    lines = [line for line in infile]

grid: list[list[int]] = [[int(depth) for depth in list(line.strip())] for line in lines]
size = len(grid[0])

visited: list[list[int]] = []
for i in range(size):
    visited.append([False] * size)

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

def calc_basin_size(row: int, col: int) -> int:
    if visited[row][col]:
        return 0

    (visited[row])[col] = True

    if grid[row][col] == 9:
        return 0
    
    res = 1
    for neigh in get_neighbors(row, col):
        res += calc_basin_size(neigh[0], neigh[1])
    return res

def get_basin_sizes_in_row(row: int) -> list[int]:
    return [calc_basin_size(row, col) for col in range(size) if not visited[row][col]]

basin_size_rows = [get_basin_sizes_in_row(row) for row in range(size)]

basin_sizes: list[int] = []
for row in basin_size_rows:
    basin_sizes = basin_sizes + row

basin_sizes.sort(reverse=True)
#print(basin_sizes[0])
#print(basin_sizes[1])
#print(basin_sizes[2])
print(basin_sizes[0] * basin_sizes[1] * basin_sizes[2])

