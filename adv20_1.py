from __future__ import annotations
import utils

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

def eval_character(character: str) -> int:
    return 1 if character == "#" else 0

def read_row(line: str) -> list[int]:
    return [eval_character(character) for character in line]

#print(eval_character("#"))
#print(eval_character("g"))
#print(eval_character("."))

algo = read_row(lines[0])
in_image = [read_row(line) for line in lines[2:]]
#print(in_image[0])
#print(in_image[-1])


#size = len(in_image[0])


def get_code(img: list[list[int]], row: int, col: int) -> int:

    def is_in_bounds(img: list[list[int]], row: int, col: int) -> bool:
        size = len(img[0])
        return row >= 0 and row < size and col >= 0 and col < size

    def get_bit_int(img: list[list[int]], row: int, col: int) -> int:
        if is_in_bounds(img, row, col):
            return img[row][col]
        return 0
    
    #def get_bit_str(row: int, col: int) -> str:
    #    return str(get_bit_int(row, col))

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

def get_pixel(img: list[list[int]], row: int, col: int) -> int:
    pix = algo[get_code(img, row, col)]
    return pix


#print(get_code(0,0))
#print(get_code(0,1))
#print(get_code(1,1))

#def get_out_pixel_by_code(code: int) -> int:
#    return algo[code]

def sum_pixels(img: list[list[int]]) -> int:
    return sum([sum(line) for line in img])

#print(sum_pixels(in_image))

def expand_image(img: list[list[int]]) -> list[list[int]]:
    new_size = len(img) + 6
    #pad_line = [0] * new_size
    mid_rows = [[0,0,0,*row,0,0,0] for row in img]
    return [[0] * new_size, [0] * new_size, [0] * new_size, *mid_rows, [0] * new_size, [0] * new_size, [0] * new_size]

def enhance_image(img: list[list[int]]) -> list[list[int]]:
    expanded_image = expand_image(img)
    out_image = expand_image(img)

    # def enhance_row(row_index: int row: list[int]) -> list[int]:
    #     return [get_pixel(new_image, )]
    
    # [ for index,row in enumerate(img)]

    out_size = len(out_image)
    for row in range(out_size):
        for col in range(out_size):
            out_image[row][col] = get_pixel(expanded_image, row, col)
    
    return out_image

def print_image(img: list[list[int]]) -> None:
    def print_row(r: list[int]) -> None:
        print("".join(["#" if p else "." for p in r]))
    for r in img:
        print_row(r)


print_image(in_image)
print(len(in_image))
print(len(in_image[0]))
print(sum_pixels(in_image))

g1 = enhance_image(in_image)
print_image(g1)
print(len(g1))
print(len(g1[0]))
print(sum_pixels(g1))

g2 = enhance_image(g1)
print_image(g2)
print(len(g2))
print(len(g2[0]))
print(sum_pixels(g2))
# print(g2)
