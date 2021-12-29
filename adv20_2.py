from __future__ import annotations
import utils

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

def eval_character(character: str) -> int:
    return 1 if character == "#" else 0

def read_row(line: str) -> list[int]:
    return [eval_character(character) for character in line]

algo = read_row(lines[0])
in_image = [read_row(line) for line in lines[2:]]


def get_code(img: list[list[int]], row: int, col: int, outside_value: int) -> int:

    def is_in_bounds(img: list[list[int]], row: int, col: int) -> bool:
        size = len(img[0])
        return row >= 0 and row < size and col >= 0 and col < size

    def get_bit_int(img: list[list[int]], row: int, col: int) -> int:
        if is_in_bounds(img, row, col):
            return img[row][col]
        return outside_value
    
    bits = [
        get_bit_int(img, row-1, col-1),
        get_bit_int(img, row-1, col),
        get_bit_int(img, row-1, col+1),
        get_bit_int(img, row, col-1),
        get_bit_int(img, row, col),
        get_bit_int(img, row, col+1),
        get_bit_int(img, row+1, col-1),
        get_bit_int(img, row+1, col),
        get_bit_int(img, row+1, col+1),
    ]

    code = int("".join([str(bit) for bit in bits]), 2)
    return code

def get_pixel(img: list[list[int]], row: int, col: int, outside_value: int) -> int:
    pix = algo[get_code(img, row, col, outside_value)]
    return pix

def sum_pixels(img: list[list[int]]) -> int:
    return sum([sum(line) for line in img])


def expand_image(img: list[list[int]], outside_value: int) -> list[list[int]]:
    new_size = len(img) + 6
    mid_rows = [[outside_value,outside_value,outside_value,*row,outside_value,outside_value,outside_value] for row in img]
    return [[outside_value] * new_size, [outside_value] * new_size, [outside_value] * new_size, *mid_rows, [outside_value] * new_size, [outside_value] * new_size, [outside_value] * new_size]

def enhance_image(img: list[list[int]], outside_value: int) -> list[list[int]]:
    expanded_image = expand_image(img, outside_value)
    out_image = expand_image(img, outside_value)

    out_size = len(out_image)
    for row in range(out_size):
        for col in range(out_size):
            out_image[row][col] = get_pixel(expanded_image, row, col, outside_value)
    
    return out_image

def print_image(img: list[list[int]]) -> None:
    def print_row(r: list[int]) -> None:
        print("".join(["#" if p else "." for p in r]))
    for r in img:
        print_row(r)

total_iterations = int(50)
outer_pixels_value = int(0)

g = in_image
for i in range(total_iterations):
    g = enhance_image(g, outer_pixels_value)
    outer_pixels_value = g[0][0]
    print(i)

print_image(g)
print(len(g[0]))
print(sum_pixels(g))
