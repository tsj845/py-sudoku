import os.path as path
import sys
from time import sleep

# ANSI container
class ANSI ():

    # reset all ansi stuff
    reset = "\x1b[0m"

    # built in colors
    red = "\x1b[38;2;255;0;0m"
    yellow = "\x1b[38;2;255;255;0m"
    lime = "\x1b[38;2;0;255;0m"
    green = "\x1b[38;2;0;200;0m"
    cyan = "\x1b[38;2;0;255;255m"
    blue = "\x1b[38;2;0;0;255m"
    violet = "\x1b[38;2;255;0;255m"
    white = "\x1b[38;2;255;255;255m"
    black = "\x1b[38;2;0;0;0m"
    normal = "\x1b[39m"

    # built in backgrounds
    bblack = "\x1b[48;2;0;0;0m"
    bnorm = "\x1b[49m"

    # printing commands
    def print (*args):
        print(*args, sep="", end="")
    
    # delete one line
    def del_above ():
        ANSI.print("\x1b[2K\x1b[1A")

    # clear screen
    def clear ():
        ANSI.print("\x1bc")

ANSI.clear()

# sudoku board input data
data : list[list[str]] = []

# sudoku board
board : list[list[int]] = []

valid_sudoku_nums = range(0, 10)

input_row = 1

def validate_sudoku_row (row : list[str]) -> bool:
    if len(row) != 9:
        return False
    for space in row:
        if space.isdigit() and int(space) in valid_sudoku_nums:
            continue
        return False
    return True

def get_sudoku_row () -> str:
    while True:
        line : str = input(f"enter row {input_row}: ")
        line = ",".join(line.strip().split(", ")).split(",")
        for i in range(len(line)):
            line[i] = line[i][0]
        if validate_sudoku_row(line):
            return line

if len(sys.argv) > 1 and path.exists(sys.argv[1]):
    with open(sys.argv[1], "r") as f:
        data = f.readlines()
    for i in range(len(data)):
        data[i] = ",".join(data[i].strip().split(", ")).split(",")
        if len(data[i]) != 9:
            raise ValueError("malformed board file input")
else:
    for i in range(9):
        data.append(get_sudoku_row())
        input_row += 1

if len(data) != 9:
    raise ValueError("malformed board input")

for i in range(9):
    board.append([])
    for j in data[i]:
        board[i].append(int(j))

ANSI.clear()

cycle_speed = 1

class Sections ():
    def __init__ (self):
        self.boxes : list[dict[int, int]] = []
        self.cols : list[dict[int, int]] = []
        self.rows : list[dict[int, int]] = []

sections = Sections()

_validation_range = range(1, 10)

def validate_rows (board : list[list[int]]) -> bool:
    for l in board:
        for t in _validation_range:
            if l.count(t) > 1:
                return False
    return True

def validate_cols (board : list[list[int]]) -> bool:
    for c in range(9):
        t = []
        for l in board:
            t.append(l[c])
        for x in _validation_range:
            if t.count(x) > 1:
                return False
    return True

def validate_boxes (board : list[list[int]]) -> bool:
    for y in range(3):
        for x in range(3):
            l = []
            for dy in range(3):
                for dx in range(3):
                    l.append(board[y+dy][x+dx])
            for t in _validation_range:
                if l.count(t) > 1:
                    return False
    return True

def validate_board (board : list[list[int]]) -> bool:
    return validate_rows(board) and validate_cols(board) and validate_boxes(board)

def check_solved (board : list[list[int]]) -> bool:
    if not validate_board(board):
        return False
    for r in board:
        for c in r:
            if c == 0:
                return False
    return True

def dump_board ():
    ANSI.clear()
    main_color = ANSI.white
    highlight = ANSI.yellow
    dash = "\u2500"
    cross = "\u253c"
    tdown = "\u252c"
    tup = "\u2534"
    dc = dash * 3 + cross
    dcy = dash * 3 + highlight + cross + main_color
    sbstart = f"{ANSI.bblack}{highlight}\u251c"
    sbend = f"{highlight}\u2524{ANSI.reset}"
    sbmid = f"{(dc*2+dcy)*2+dc*2+dash*3}"
    topbound = f"{ANSI.bblack}{highlight}\u250c{(dash*3+tdown)*8+dash*3}\u2510{ANSI.reset}"
    sepbound = f"{sbstart}{main_color}{sbmid}{sbend}"
    boxbound = f"{sbstart}{(dash*3+cross)*8+dash*3}{sbend}"
    botbound = f"{ANSI.bblack}{highlight}\u2514{(dash*3+tup)*8+dash*3}\u2518{ANSI.reset}"
    print(topbound)
    ps = False
    for j in range(len(board)):
        l = board[j]
        if ps:
            print(boxbound if j % 3 == 0 else sepbound)
        else:
            ps = True
        ANSI.print(ANSI.bblack)
        for i in range(len(l)):
            s = l[i]
            ANSI.print(f"{highlight if i % 3 == 0 else main_color}\u2502 {ANSI.green}{s} ")
        print(f"{highlight}\u2502{ANSI.reset}")
    print(botbound)
    print(ANSI.reset)

def segment_boxes ():
    pass

def segment_rows ():
    pass

def segment_cols ():
    pass

def segment ():
    sections.boxes = []
    sections.rows = []
    sections.cols = []
    segment_boxes()
    segment_cols()
    segment_rows()

def solve_step ():
    segment()

while not check_solved(board):
    solve_step()
    dump_board()
    sleep(cycle_speed)

dump_board()