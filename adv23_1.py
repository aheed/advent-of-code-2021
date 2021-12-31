
#  01234567890
#0 01 2 3 4 56 
#1   7 8 9 0
#2   1 2 3 4


nof_spots = int(15)
spots = ["."] * nof_spots

# given input:
#############
#...........#
###D#B#D#A###
  #C#C#A#B#
  #########
spots[7] = "D"
spots[8] = "B"
spots[9] = "D"
spots[10] = "A"
spots[11] = "C"
spots[12] = "C"
spots[13] = "A"
spots[14] = "B"

# example (answer is 12521):
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
# spots[7] = "B"
# spots[8] = "C"
# spots[9] = "B"
# spots[10] = "D"
# spots[11] = "A"
# spots[12] = "D"
# spots[13] = "C"
# spots[14] = "A"

### TEMP!!!
# spots[11] = "A"
# spots[8] = "B"
# spots[9] = "C"
# spots[4] = "D"
# spots[14] = "A"
# spots[12] = "B"
# spots[13] = "C"
# spots[10] = "D"
###

target_spots = ["."] * nof_spots

# given:
#############
#...........#
###D#B#D#A###
  #C#C#A#B#
  #########

target_spots[7] = "A"
target_spots[8] = "B"
target_spots[9] = "C"
target_spots[10] = "D"
target_spots[11] = "A"
target_spots[12] = "B"
target_spots[13] = "C"
target_spots[14] = "D"


print(spots)

def get_spot_index(x: int, y:int) -> int:
  if y == 0:
    if x == 0:
      return 0
    if x == 1:
      return 1
    if x == 3:
      return 2
    if x == 5:
      return 3
    if x == 7:
      return 4
    if x == 9:
      return 5
    if x == 10:
      return 6
  if y == 1:
    if x == 2:
      return 7
    if x == 4:
      return 8
    if x == 6:
      return 9
    if x == 8:
      return 10
  if y == 2:
    if x == 2:
      return 11
    if x == 4:
      return 12
    if x == 6:
      return 13
    if x == 8:
      return 14
  return -1

spot_coords = [(0,0), (1,0), (3,0), (5,0), (7,0), (9,0), (10,0),
               (2,1), (4,1), (6,1), (8,1),
               (2,2), (4,2), (6,2), (8,2)]

step_costs = {"A":1, "B":10, "C":100, "D":1000}
room_x = {"A":2, "B":4, "C":6, "D":8}
corridor_spots = [i for i in range(0,7)]
room_spots = [i for i in range(7,15)]

def get_coords(index: int) -> tuple[int, int]:
  return spot_coords[index]


#def is_target_position(spots: list[str]) -> bool:
#  return spots[7] == "A" and spots[8] == "B" and spots[9] == "C" and spots[10] == "D" and spots[11] == "A" and spots[12] == "B" and spots[13] == "C" and spots[14] == "D"

def is_target_position(spots: list[str]) -> bool:
  return next((False for index in range(7,15) if spots[index] != target_spots[index]), True)

infinity = int(1000000)
best_so_far = infinity
prunes = int(0)

def min_energy_to_reach_target(energy_spent: int, spots: list[str]) -> int:
  global best_so_far
  global prunes

  if energy_spent >= best_so_far:
    #print("pruned!")
    prunes += 1
    return energy_spent

  if is_target_position(spots):
    if energy_spent < best_so_far:
      best_so_far = energy_spent
      print(f"new best: {best_so_far} p:{prunes}")
    return energy_spent

  #move out
  for index in room_spots:
    amphi_type = spots[index]
    cost = int(0)
    x,y = spot_coords[index]
    
    if amphi_type != "." and (amphi_type != target_spots[index] or (y == 1 and target_spots[get_spot_index(x, 2)] != spots[get_spot_index(x, 2)])):
      # move up
      ok = True
      while y > 0:
        cost += step_costs[amphi_type]
        y -= 1
        new_spot = get_spot_index(x, y)
        ok = new_spot == -1 or spots[new_spot] == "."
        if not ok:
          break
      if not ok:
        continue
      cost_after_exit = cost
      
      # move left from room exit
      while x > 0:
        cost += step_costs[amphi_type]
        x -= 1
        new_spot = get_spot_index(x, y)
        ok = new_spot == -1 or spots[new_spot] == "."
        if not ok:
          break

        if new_spot != -1:
          new_position = spots[:]
          new_position[new_spot] = amphi_type
          new_position[index] = "."
          best_so_far = min(best_so_far, min_energy_to_reach_target(energy_spent + cost, new_position))
      
      
      # move right from room exit
      x,y = spot_coords[index]
      y = 0
      cost = cost_after_exit

      while x < 10:
        cost += step_costs[amphi_type]
        x += 1
        new_spot = get_spot_index(x, y)
        ok = new_spot == -1 or spots[new_spot] == "."
        if not ok:
          break

        if new_spot != -1:
          new_position = spots[:]
          new_position[new_spot] = amphi_type
          new_position[index] = "."
          best_so_far = min(best_so_far, min_energy_to_reach_target(energy_spent + cost, new_position))

  #move in
  for index in corridor_spots:
    amphi_type = spots[index]
    #cost = int(0)
    ok = True
    if amphi_type != ".":
      start_x,_ = spot_coords[index]
      target_x = room_x[amphi_type]
      #minx = min(start_x, target_x)
      #maxx = max(start_x, target_x)
      if start_x < target_x:
        minx = start_x + 1
        maxx = target_x + 1
      else:
        minx = target_x
        maxx = start_x
      for x in range(minx, maxx):
        new_spot = get_spot_index(x, 0)
        ok = new_spot == -1 or spots[new_spot] == "."
        if not ok:
          break
      if not ok:
        continue

      # move down
      if spots[get_spot_index(target_x, 1)] == "." and (spots[get_spot_index(target_x, 2)] == "." or spots[get_spot_index(target_x, 2)] == amphi_type):
        if spots[get_spot_index(target_x, 2)] == ".":
          target_y = 2
        else:
          target_y = 1
        
        cost = (maxx - minx + target_y) * step_costs[amphi_type]
        new_position = spots[:]
        new_spot_index = get_spot_index(target_x, target_y)
        assert(new_position[new_spot_index] == ".")
        new_position[new_spot_index] = amphi_type
        assert(new_position[index] == amphi_type)
        new_position[index] = "."
        best_so_far = min(best_so_far, min_energy_to_reach_target(energy_spent + cost, new_position))

  return best_so_far

res = min_energy_to_reach_target(0, spots)
print(f"p: {prunes}")
print(res)