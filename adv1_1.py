import utils

depths = utils.get_ints_from_in_file_lines()

increases = 0

prev = depths[0]
for depth in depths[1:]:
    if (depth > prev):
        increases += 1
    prev = depth

print(increases)
