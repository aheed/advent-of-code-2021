
positions = int(9)

class Deterministic_Die:
    last_val: int = 0

    def dice_next_val(self) -> int:
        self.last_val = (self.last_val % 100) + 1
        return self.last_val

def pos_after_steps(original_pos: int, steps: int) -> int:
    return (original_pos + steps) % 10

def pos_after_turn(original_pos: int, die: Deterministic_Die) -> int:
    d1 = die.dice_next_val()
    d2 = die.dice_next_val()
    d3 = die.dice_next_val()
    return pos_after_steps(original_pos, d1 + d2 +d3)

def play_game(p1_start: int, p2_start: int) -> tuple[int, int]:
    p1_pos = p1_start
    p2_pos = p2_start
    p1_score = int(0)
    p2_score = int(0)
    nof_rolls = int(0)
    die = Deterministic_Die()

    while p1_score < 1000 and p2_score < 1000:
        nof_rolls += 3
        p1_pos = pos_after_turn(p1_pos, die)
        p1_score += (p1_pos + 1)
        if p1_score >= 1000:
            break
        nof_rolls += 3
        p2_pos = pos_after_turn(p2_pos, die)
        p2_score += (p2_pos + 1)

    return (min(p1_score, p2_score), nof_rolls)

p1_s = 5 #zero based, the input given is 6
p2_s = 3 #zero based, the input given is 4
# p1_s = 3 #zero based, the example given is 6
# p2_s = 7 #zero based, the example given is 8

loser_score, rolls = play_game(p1_s, p2_s)

print(loser_score, rolls)
print(loser_score * rolls)


