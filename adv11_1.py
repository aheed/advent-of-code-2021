import utils


with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

energy: list[list[int]] = [[int(depth) for depth in list(line.strip())] for line in lines]
size = len(energy[0])
total_flashes = int(0)

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
    add_if_in_bounds(row - 1, col - 1)
    add_if_in_bounds(row + 1, col - 1)
    add_if_in_bounds(row - 1, col + 1)
    add_if_in_bounds(row + 1, col + 1)
    return neigh

def calc_energy_step():

    global energy
    global total_flashes

    flashed: list[list[int]] = []
    for _ in range(size):
        flashed.append([False] * size)
    
    for row in range(size):
            for col in range(size):
                energy[row][col] += 1

    calc_pending = True

    while (calc_pending):
        calc_pending = False
        for row in range(size):
            for col in range(size):
                if (energy[row][col] > 9 and not flashed[row][col]):
                    flashed[row][col]= True
                    total_flashes += 1
                    calc_pending = True
                    for neigh in get_neighbors(row, col):
                        energy[neigh[0]][neigh[1]] += 1

    for row in range(size):
        for col in range(size):
            if flashed[row][col]:
                energy[row][col] =0

for _ in range(100):
    calc_energy_step()
#print(energy)
print(total_flashes)
