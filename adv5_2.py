import utils

infile = utils.get_in_file()
lines = [line for line in infile]
infile.close()

def get_point(text: str) -> tuple[int, int]:
    coord_texts = text.split(",")
    return (int(coord_texts[0]), int(coord_texts[1]))

def create_vent_line(text: str) -> list[tuple[int, int]]:
    point_texts = text.split(" -> ")

    p1 = get_point(point_texts[0])
    p2 = get_point(point_texts[1])
    
    res : list[tuple[int, int]] = []
    if (p1[0] == p2[0]):
        if(p1[1] < p2[1]):
            start_point = p1
            end_point = p2
        else:
            start_point = p2
            end_point = p1
        for y in range(start_point[1], end_point[1]+1):
            res.append((start_point[0], y))
    if (p1[1] == p2[1]):
        if(p1[0] < p2[0]):
            start_point = p1
            end_point = p2
        else:
            start_point = p2
            end_point = p1
        for x in range(start_point[0], end_point[0]+1):
            res.append((x, start_point[1]))
    if ( abs(p1[0] - p2[0]) == abs(p1[1] - p2[1])):
        if (p1[0] < p2[0]):
            start_point = p1
            end_point = p2
        else:
            start_point = p2
            end_point = p1
        if (start_point[1] < end_point[1]):
            yincr = 1
        else:
            yincr = -1
        y = start_point[1]
        for x in range(start_point[0], end_point[0]+1):
            res.append((x, y))
            y += yincr
    return res


vent_lines: list[list[tuple[int, int]]] = [create_vent_line(line) for line in lines]

vent_sets = [set(vent_line) for vent_line in vent_lines]

all_vents_set: set[tuple[int, int]] = set([])
for vent_set in vent_sets:
    all_vents_set.update(vent_set)

#print(type(all_vents_set))
#print(len(all_vents_set))

all_vents_set2: set[tuple[int, int]] = set([])
duplicates: set[tuple[int, int]] = set([])

for vent_set in vent_sets:
    new_duplicates = all_vents_set2.intersection(vent_set)
    duplicates.update(new_duplicates)
    all_vents_set2.update(vent_set)

#print(len(all_vents_set2))
print(len(duplicates))
