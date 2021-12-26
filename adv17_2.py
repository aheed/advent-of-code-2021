from functools import cache

min_x = 175
max_x = 227
min_y = -134
max_y = -79

# min_x = 20
# max_x = 30
# min_y = -10
# max_y = -5

min_vx0 = 15
max_vx0 = max_x
min_vy0 = min_y
max_vy0 = -min_y-1
max_t = 270

def is_in_target_area(x: int, y: int) -> bool:
    return x >= min_x and x <= max_x and y >= min_y and y <= max_y

@cache
def calc_x(vx0: int, t: int) -> int:
    vx = vx0
    x = 0
    for _ in range(t):
        x += vx
        if vx > 0:
            vx -= 1
    return x

@cache
def calc_y(vy0: int, t: int) -> int:
    vy = vy0
    y = 0
    for _ in range(t):
        y += vy
        vy -= 1
    return y

res = int(0)
for vy0 in range(min_vy0, max_vy0+1):
    for vx0 in range(min_vx0, max_vx0+1):
        hit = False
        for t in range(max_t):
            x = calc_x(vx0, t)
            y = calc_y(vy0, t)
            if is_in_target_area(x, y):
                hit = True
                res += 1
                #print(x, y)
                break

print(res)

