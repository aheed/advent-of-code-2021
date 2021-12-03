import utils

lines = utils.get_in_file()

gamma = 0
epsilon = 0
for pos in range(12):
    sum = 0
    ints = utils.get_ints_from_in_file_lines(2)
    for entry in ints:
        sum += (entry >> pos) % 2
    bit_at_pos = sum > len(ints) / 2 
    gamma += int(bit_at_pos) << pos
    epsilon += int(not bit_at_pos) << pos
    print(sum, bit_at_pos)

print(gamma)
print(epsilon)
print(gamma * epsilon)

