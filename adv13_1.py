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

fold_x_coord = 655
#fold_x_coord = 7

post_fold_dots: dict[int, tuple[int, int]] = {}
for (hash, coords) in dots.items():
    new_coords = fold_at_x(coords, fold_x_coord)
    # if hash_dot(new_coords) in post_fold_dots:
    #     print("overlap")
    post_fold_dots[hash_dot(new_coords)] = new_coords

#print(post_fold_dots)
#print(len(dots))
print(len(post_fold_dots))