from dataclasses import dataclass
from functools import cache
import utils

@dataclass(frozen=True)
class Cell:
    row: int
    col: int

with utils.get_in_file() as infile:
    lines = [line for line in infile]

initial_grid: list[list[int]] = [[int(depth) for depth in list(line.strip())] for line in lines]
initial_size = len(initial_grid[0])
print(initial_size)

def get_grid_val(row: int, col: int) -> int:
    to_add = int(row / initial_size) + int(col / initial_size)
    #return (initial_grid[row % initial_size][col % initial_size] + to_add) % 10
    return (((initial_grid[row % initial_size][col % initial_size] + to_add) - 1) % 9) + 1

x_factor = 5
size = initial_size * x_factor
print(size)

grid: list[list[int]] = [[0] * size for _ in range(size)]
for row in range(size):
    for col in range(size):
        grid[row][col] = get_grid_val(row, col)

print(grid)


def is_in_bounds(row: int, col: int) -> bool:
    return row >= 0 and row < size and col >= 0 and col < size

def get_neighbors_old(row: int, col: int) -> list[Cell]:
    neigh: list[Cell] = []

    def add_if_in_bounds(row: int, col: int):
        if is_in_bounds(row, col):
            neigh.append(Cell(row, col))
    
    add_if_in_bounds(row - 1, col)
    add_if_in_bounds(row + 1, col)
    add_if_in_bounds(row, col - 1)
    add_if_in_bounds(row, col + 1)    
    return neigh

def get_neighbors(cell: Cell) -> list[Cell]:
    neigh: list[Cell] = []

    def add_if_in_bounds(row: int, col: int):
        if is_in_bounds(row, col):
            neigh.append(Cell(row, col))
    
    add_if_in_bounds(cell.row - 1, cell.col)
    add_if_in_bounds(cell.row + 1, cell.col)
    add_if_in_bounds(cell.row, cell.col - 1)
    add_if_in_bounds(cell.row, cell.col + 1)
    return neigh

infinity = int(1000000)
prel_res: list[list[int]] = [[infinity] * size for _ in range(size)]
unvisited_cells: set[Cell] = set([])

def set_prel_res(cell: Cell, res: int) -> None:
    global prel_res
    global unvisited_cells
    
    prel_res[cell.row][cell.col] = res
    unvisited_cells.add(cell)

def update_prel_res(cell: Cell, res: int) -> None:
    global prel_res
    global unvisited_cells
    
    if res < prel_res[cell.row][cell.col]:
        prel_res[cell.row][cell.col] = res
        unvisited_cells.add(cell)

def calc_risks() -> None:
    global prel_res
    global unvisited_cells

    start_cell = Cell(0, 0)
    set_prel_res(start_cell, 0)

    def visit_cell(cell: Cell) -> None:
        #print(cell)
        current_risk = prel_res[cell.row][cell.col]
        #neighbors = [neighbor for neighbor in get_neighbors(cell) if neighbor in unvisited_cells]
        neighbors = get_neighbors(cell)
        for neighbor in neighbors:
            update_prel_res(neighbor, current_risk + grid[neighbor.row][neighbor.col])
        unvisited_cells.remove(cell)

    while True:
        if unvisited_cells == set():
            break

        next_cell = sorted(unvisited_cells, key = lambda cell: prel_res[cell.row][cell.col])[0]
        visit_cell(next_cell)


calc_risks()
#print(prel_res)
print(prel_res[size-1][size-1])


    