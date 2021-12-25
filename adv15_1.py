from dataclasses import dataclass
import utils

@dataclass(frozen=True)
class Cell:
    row: int
    col: int

with utils.get_in_file() as infile:
    lines = [line for line in infile]

initial_grid = [[int(depth) for depth in list(line.strip())] for line in lines]
initial_size = len(initial_grid[0])
#print(initial_size)

size = initial_size
#print(size)

grid = initial_grid
#print(grid)

def is_in_bounds(row: int, col: int) -> bool:
    return row >= 0 and row < size and col >= 0 and col < size

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
prel_res = [[infinity] * size for _ in range(size)]
unvisited_cells: set[Cell] = set([])

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
    update_prel_res(start_cell, 0)

    def visit_cell(cell: Cell) -> None:
        current_risk = prel_res[cell.row][cell.col]
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


    