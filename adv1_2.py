import utils

depths = utils.get_ints_from_in_file_lines()

increases = 0
window_size = 3

for i in range(len(depths) - window_size + 1):
    window = depths[i:i+window_size]
    avg = sum(window)
    if (i > 0 and avg > prev):
        increases += 1
    prev = avg

print(increases)
