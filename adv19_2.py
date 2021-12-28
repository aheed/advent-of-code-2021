from __future__ import annotations
from dataclasses import dataclass
import math
import utils


with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

#print(lines)

l1: list[list[str]] = []
l2: list[str] = []

for line in lines:
    if len(line) < 3:
        if len(l2) > 0:
            l1.append(l2)
            l2 = []
    elif "scanner" in line:
        pass
    else:
        l2.append(line)

print(len(l1))
print(l1[0])
print(l1[-1])

@dataclass(frozen=True)
class Point:
    coords: list[int]

    def __hash__(self):
        return self.coords[0] * 10000 * 10000 + self.coords[1] * 10000 + self.coords[2]

@dataclass(frozen=True)
class Orientation:
    index: int #0-5
    x_dir: int #-1, 1
    y_dir: int #-1, 1
    z_dir: int #-1, 1

@dataclass
class Scanner:
    #orientation: Orientation | None #scanner0 coordinate system
    #position: Point | None #scanner0 coordinate system
    beacons: list[Point] #local coordinate system
    name: str

def read_point(line: str) -> Point:
    composants_str = line.split(",")
    composants_int = [int(c) for c in composants_str]
    return Point(composants_int)

nof_read_scanners = int(0)
def read_scanner(lines: list[str]) -> Scanner:
    global nof_read_scanners
    beacs = [read_point(p) for p in lines]
    new_scanner= Scanner(beacs, f"scanner{nof_read_scanners}")
    nof_read_scanners += 1
    return new_scanner

raw_scanners = [read_scanner(l2) for l2 in l1]

print(len(raw_scanners))
print(raw_scanners[0])

 # declare scanner0 as normalized
normalized_scanners = [raw_scanners.pop(0)]
#normalized_scanners = [raw_scanners.pop(21)] #TEMP!!!

orientations = [[0,1,2], [0,2,1], [1,0,2], [1,2,0], [2,0,1], [2,1,0]]

def normalize_beacon(raw: Point, orientation: Orientation) -> Point:
    vector = orientations[orientation.index]
    return Point([raw.coords[vector[0]] * orientation.x_dir, raw.coords[vector[1]] * orientation.y_dir, raw.coords[vector[2]] * orientation.z_dir])

def normalize_scanner(raw: Scanner, orientation: Orientation) -> Scanner:
    beacs = [normalize_beacon(b, orientation) for b in raw.beacons]
    return Scanner(beacs, raw.name)

scanner_distances: dict[str, Point] = {normalized_scanners[0].name: Point([0,0,0])}

last_nof_matches = 0
while len(raw_scanners) > 0:
    if len(normalized_scanners) == last_nof_matches:
        print("give up")
        break
    last_nof_matches = len(normalized_scanners)
    print("trying to match...")
    scanner_matched = False
    for n_scanner_index,n_scanner in enumerate(normalized_scanners):
        for r_scanner_index,r_scanner in enumerate(raw_scanners):
            for orientation_index in range(6):
                for x_dir in [-1, 1]:
                    for y_dir in [-1, 1]:
                        for z_dir in [-1, 1]:
                            prel_norm_scanner = normalize_scanner(r_scanner, Orientation(orientation_index, x_dir, y_dir, z_dir))
                            #nof_matching_beacons = int(0)
                            beacon_distances: dict[Point, int] = {}
                            for origin_beacon in n_scanner.beacons:
                                for distant_beacon in prel_norm_scanner.beacons:
                                    dist = Point([c_origin - c_dist for c_origin,c_dist in zip(origin_beacon.coords, distant_beacon.coords)])
                                    nof_beacons_at_dist = beacon_distances.get(dist, 0) + 1
                                    beacon_distances[dist] = nof_beacons_at_dist
                            #max_nof_beacons_at_any_dist = sorted(beacon_distances.values())[-1]
                            dist_and_max_nof_beacons_at_any_dist = sorted(beacon_distances.items(), key= lambda item: item[1])[-1]
                            max_nof_beacons_at_any_dist = dist_and_max_nof_beacons_at_any_dist[1]

                            if max_nof_beacons_at_any_dist > 1:
                                print(f"n_scanner_index: {n_scanner_index} r_scanner_index: {r_scanner_index}  max_nof_beacons_at_any_dist: {max_nof_beacons_at_any_dist}")
                            if max_nof_beacons_at_any_dist >= 12:
                            #if max_nof_beacons_at_any_dist >= 6:
                                print("matching scanners!!")
                                normalized_scanners.append(prel_norm_scanner)
                                raw_scanners.pop(r_scanner_index)
                                dist_to_n_scanner = scanner_distances[n_scanner.name]
                                dist_to_prel_norm_scanner = Point([c1 + c2 for c1,c2 in zip(dist_to_n_scanner.coords, dist_and_max_nof_beacons_at_any_dist[0].coords)])
                                scanner_distances[prel_norm_scanner.name] = dist_to_prel_norm_scanner
                                scanner_matched = True
                                break
                        if scanner_matched:
                            break
                    if scanner_matched:
                        break
                if scanner_matched:
                    break
            if scanner_matched:
                break
        if scanner_matched:
            break

print(raw_scanners)    
print(len(normalized_scanners))
print(len(raw_scanners))
print(len(scanner_distances))
print(scanner_distances)

norm_beacons: set[Point] = set([])

for sc in normalized_scanners:
    sc_dist = scanner_distances[sc.name]
    for beacon in sc.beacons:
        norm_beacon = Point([c_sc + c_bea for c_sc,c_bea in zip(sc_dist.coords, beacon.coords)])
        norm_beacons.add(norm_beacon)

print(len(norm_beacons))
#print(len(raw_scanners[0].beacons))


##############
def manhattan(p1: Point, p2: Point) -> int:
    return sum([abs(c1 - c2) for c1,c2 in zip(p1.coords, p2.coords)])

max_manhattan = 0
for p1 in scanner_distances.values():
    for p2 in scanner_distances.values():
        candidate = manhattan(p1, p2)
        print(candidate)
        if candidate > max_manhattan:
            max_manhattan = candidate

print(max_manhattan)