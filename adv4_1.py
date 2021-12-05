import utils

infile = utils.get_in_file()
lines = [line for line in infile]
infile.close()

#print(lines)

drawn_numbers = [int(num) for num in lines[0].split(',')]
#print(drawn_numbers)

infile = utils.get_in_file()
all_boards_texts = infile.read().split('\n\n')[1:]


class BingoNumber():
    drawn: bool
    def __init__(self, numval: int):
        self.numval = numval
        self.drawn = False
    
    def __str__(self):
        return f'{self.numval} {self.drawn}'

    def __repr__(self):
        return self.__str__()

class Board():
    last_drawn: int

    def __init__(self, fives: list[list[BingoNumber]]):
        self.fives = fives
        
    def draw_number(self, number: int):
        for row in self.fives:
            for bingo_num in row:
                if (bingo_num.numval == number):
                    bingo_num.drawn = True
                    self.last_drawn = number

    def got_bingo(self) -> bool:
        for col in range(5):
            all_drawn = True
            for row in range(5):
                all_drawn = all_drawn and self.fives[row][col].drawn
            if (all_drawn):
                return True

        for row in range(5):
            all_drawn = True
            for col in range(5):
                all_drawn = all_drawn and self.fives[row][col].drawn
            if (all_drawn):
                return True

        return False

    def calc_score(self) -> int:
        sum = 0
        for row in range(5):
            for col in range(5):
                if (not self.fives[row][col].drawn):
                    sum += self.fives[row][col].numval
        return sum * self.last_drawn

def create_row(text: str) -> list[BingoNumber]:
    numbers = text.strip().split(' ')
    return [BingoNumber(int(num)) for num in numbers if len(num) > 0]

def create_rows(text: str) -> list[list[BingoNumber]]:
    return [create_row(five_str) for five_str in text.split('\n')]


def create_board(text: str) -> Board:
    rows = create_rows(text)
    #cols = create_cols(text)
    return Board(rows)

boards = [create_board(board_text) for board_text in all_boards_texts]

def get_first_bingo_board_index() -> int:
    for drawn_num in drawn_numbers:
        board_index = 0
        for board in boards:
            board.draw_number(drawn_num)
            if (board.got_bingo()):
                return board_index
            board_index += 1
    raise Exception("should not get here")

best_board_index = get_first_bingo_board_index()
#print("Bingo", best_board_index)

best_board = boards[best_board_index]
print(best_board.calc_score())