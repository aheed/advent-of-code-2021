from dataclasses import dataclass
import utils


with utils.get_in_file() as infile:
    lines = [line for line in infile]

grid: list[list[int]] = [[int(depth) for depth in list(line.strip())] for line in lines]

size = len(grid[0])

def is_in_bounds(row: int, col: int) -> bool:
    return row >= 0 and row < size and col >= 0 and col < size

def get_neighbors(row: int, col: int) -> list[int]:
    neigh: list[int] = []

    def add_if_in_bounds(row: int, col: int):
        if is_in_bounds(row, col):
            neigh.append(grid[row][col])
    
    add_if_in_bounds(row - 1, col)
    add_if_in_bounds(row + 1, col)
    add_if_in_bounds(row, col - 1)
    add_if_in_bounds(row, col + 1)    
    return neigh

def is_low_point(row: int, col: int) -> bool:
    low_val = grid[row][col]
    return next((False for neigh in get_neighbors(row, col) if neigh <= low_val), True)

def get_low_points_in_row(row: int) -> list[int]:
    return [grid[row][col] for col in range(size) if is_low_point(row, col)]

low_point_rows = [get_low_points_in_row(row) for row in range(size)]
#print(low_point_rows[0])

low_points: list[int] = []
for row in low_point_rows:
    low_points = low_points + row

risk_vals = [height + 1 for height in low_points]
print(sum(risk_vals))