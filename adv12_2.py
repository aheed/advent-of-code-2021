import utils


with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

tunnels: dict[str, set[str]] = {}

for line in lines:
    (src_cave, dst_cave) = tuple(line.split("-"))
    if src_cave in tunnels:
        tunnels[src_cave].add(dst_cave)
    else:
        tunnels[src_cave] = set([dst_cave])

    if dst_cave in tunnels:
        tunnels[dst_cave].add(src_cave)
    else:
        tunnels[dst_cave] = set([src_cave])

#print(tunnels)


def calc_routes(src_cave: str, visited_caves: set[str], double_small_visit: bool) -> int:
    if src_cave == "end":
        return 1
    
    newly_visited_caves = set([])
    new_double_small_visit = double_small_visit

    if src_cave.islower():
        if src_cave in visited_caves:
            if not double_small_visit and src_cave != "start":
                new_double_small_visit = True
            else:
                return 0
        newly_visited_caves.add(src_cave)

    visited = visited_caves.union(newly_visited_caves)

    res = int(0)
    if src_cave in tunnels:
        for destination in tunnels[src_cave]:
            res += calc_routes(destination, visited, new_double_small_visit)
    
    return res

result =  calc_routes("start", set([]), False)
print(result)