from functools import cache

def pos_after_steps(original_pos: int, steps: int) -> int:
    return (original_pos + steps) % 10

@cache
def calc_nof_universes(p1_start: int, p2_start: int, p1_score: int, p2_score: int, p1s_turn: bool) -> tuple[int, int]:
    if p1_score >= 21:
        return (1, 0)
    
    if p2_score >= 21:
        return (0, 1)

    p1_total_wins = int(0)
    p2_total_wins = int(0)

    for d1 in range(1,4):
        for d2 in range(1,4):
            for d3 in range(1,4):
                if p1s_turn:
                    p1_pos = pos_after_steps(p1_start, d1+d2+d3)
                    p1_sc = p1_score + (p1_pos + 1)
                    p1_wins, p2_wins = calc_nof_universes(p1_pos, p2_start, p1_sc, p2_score, False)
                    p1_total_wins += p1_wins
                    p2_total_wins += p2_wins
                else:
                    p2_pos = pos_after_steps(p2_start, d1+d2+d3)
                    p2_sc = p2_score + (p2_pos + 1)
                    p1_wins, p2_wins = calc_nof_universes(p1_start, p2_pos, p1_score, p2_sc, True)
                    p1_total_wins += p1_wins
                    p2_total_wins += p2_wins
    return (p1_total_wins, p2_total_wins)
    
p1_s = 5 #zero based, the input given is 6
p2_s = 3 #zero based, the input given is 4
#p1_s = 3 #zero based, the example given is 6
#p2_s = 7 #zero based, the example given is 8

p1w, p2w = calc_nof_universes(p1_s, p2_s, 0, 0, True)
print(max(p1w, p2w))
