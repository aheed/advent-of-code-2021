import utils
from enum import Enum



class SubmarineDirectionEnum(Enum):
    FORWARD = 1
    UP = 2
    DOWN = 3
    UNKNOWN = 101

class SubmarineMove():
    def __init__(self, direction, distance):
        self.direction = direction
        self.distance = distance
    
    def get_delta_depth(self):
        if (self.direction == SubmarineDirectionEnum.DOWN):
            return self.distance
        if (self.direction == SubmarineDirectionEnum.UP):
            return -self.distance
        return 0

    def get_delta_forward(self):
        if (self.direction == SubmarineDirectionEnum.FORWARD):
            return self.distance
        return 0

def create_submarine_direction(line) -> SubmarineDirectionEnum:
    if(line == "forward"):
        return SubmarineDirectionEnum.FORWARD
    if(line == "up"):
        return SubmarineDirectionEnum.UP
    if(line == "down"):
        return SubmarineDirectionEnum.DOWN

def create_submarine_move(line) -> SubmarineMove:
    parts =  line.split(" ")
    direction = create_submarine_direction(parts[0])
    distance = int(parts[1])
    return SubmarineMove(direction, distance)


lines = utils.get_in_file()
moves = [create_submarine_move(line) for line in lines]

depth = 0
forward = 0
for move in moves:
    print(move.direction, move.distance)
    depth += move.get_delta_depth()
    forward += move.get_delta_forward()

print(depth)
print(forward)
print(depth * forward)