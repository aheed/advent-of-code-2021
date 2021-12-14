import utils

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

dots: dict[int, tuple[int, int]] = {}

def hash_dot(dot: tuple[int, int]) -> int:
    return dot[0] * 10000 + dot[1]

for line in lines:
    coords = line.split(",")
    dot = (int(coords[0]), int(coords[1]))
    dots[hash_dot(dot)] = dot

#print(dots)

def fold_at_y(dot: tuple[int, int], fold_y: int) -> tuple[int, int]:
    if dot[1] < fold_y:
        y = dot[1]
    else:
        y = 2 * fold_y - dot[1]
    return (dot[0], y)

def fold_at_x(dot: tuple[int, int], fold_x: int) -> tuple[int, int]:
    if dot[0] < fold_x:
        x = dot[0]
    else:
        x = 2 * fold_x - dot[0]
    return (x, dot[1])

def fold_all_at_x(dots_to_fold: dict[int, tuple[int, int]], fold_x: int) -> dict[int, tuple[int, int]]:
    post_fold_dots: dict[int, tuple[int, int]] = {}
    for (_, coords) in dots_to_fold.items():
        new_coords = fold_at_x(coords, fold_x)
        post_fold_dots[hash_dot(new_coords)] = new_coords
    return post_fold_dots

def fold_all_at_y(dots_to_fold: dict[int, tuple[int, int]], fold_y: int) -> dict[int, tuple[int, int]]:
    post_fold_dots: dict[int, tuple[int, int]] = {}
    for (_, coords) in dots_to_fold.items():
        new_coords = fold_at_y(coords, fold_y)
        post_fold_dots[hash_dot(new_coords)] = new_coords
    return post_fold_dots


dots2 = fold_all_at_x(dots, 655)
dots2 = fold_all_at_y(dots2, 447)
dots2 = fold_all_at_x(dots2, 327)
dots2 = fold_all_at_y(dots2, 223)
dots2 = fold_all_at_x(dots2, 163)
dots2 = fold_all_at_y(dots2, 111)
dots2 = fold_all_at_x(dots2, 81)
dots2 = fold_all_at_y(dots2, 55)
dots2 = fold_all_at_x(dots2, 40)
dots2 = fold_all_at_y(dots2, 27)
dots2 = fold_all_at_y(dots2, 13)
dots2 = fold_all_at_y(dots2, 6)

#print(len(dots2))

max_x = max([coords[0] for coords in dots2.values()])
max_y = max([coords[1] for coords in dots2.values()])

out_str = ""
for y in range(max_y + 1):
    for x in range(max_x + 1):
        if hash_dot((x, y)) in dots2:
            out_str += "X"
        else:
            out_str += " "
    out_str += "\n"

print(out_str)