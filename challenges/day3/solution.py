#! /usr/bin/python3

class Number:
    def __init__(self, no, row, col, len):
        self.no = no
        self.row = row
        self.col = col
        self.len = len


def is_numeral(c):
    return c in "1234567890"


def is_dot(c):
    return c == "."


def is_asterisk(c):
    return c == "*"


def parse_input(inp):
    symbols = []
    numbers = []
    gears = []
    number_str = ""
    for i, row in enumerate(inp.split("\n")):
        symbols.append([])
        for j, c in enumerate("." + row + "."):
            if is_numeral(c):
                number_str += c
            elif number_str != "":
                cl = j - len(number_str)
                ln = len(number_str)
                numbers.append(Number(int(number_str), i, cl, ln))
                number_str = ""
            if not is_numeral(c) and not is_dot(c):
                symbols[-1].append(True)
            else:
                symbols[-1].append(False)
            if is_asterisk(c):
                gears.append((i, j))
    # add a column at the beginning and end
    symbols = [[False] + row + [False] for row in symbols]
    for n in numbers:
        n.col += 1
    gears = [(g[0], g[1]+1) for g in gears]
    
    # add a row at the beginning and end
    symbols = [len(symbols[0])*[False]] + symbols + [len(symbols[-1])*[False]]
    for n in numbers:
        n.row += 1
    gears = [(g[0]+1, g[1]) for g in gears]

    return symbols, numbers, gears


def symbol_in_square(symbols, x0, y0, dx, dy):
    res = False
    for x in range(x0, x0+dx):
        res = res or True in symbols[x][y0:y0+dy]
    return res


def get_number_board(numbers, x, y):
    board = [y*[None] for j in range(x)]
    for n in numbers:
        board[n.row][n.col:n.col+n.len] = n.len*[n]
    return board


def get_numbers_in_square(number_board, x, y, dl):
    res_set = set()
    for i in range(x, x+dl):
        for j in range(y, y+dl):
            if number_board[i][j] is not None:
                res_set.add(number_board[i][j])
    return [itm for itm in res_set]


def solution1(symbols, numbers):
    res = 0
    for n in numbers:
        x, y, ln = n.row, n.col, n.len
        if symbol_in_square(symbols, x-1, y-1, 3, ln+2):
            res += n.no
    return res

def solution2(symbols, numbers, gears):
    res = 0
    nb = get_number_board(numbers, len(symbols), len(symbols[0]))
    for g in gears:
        ad_nos = get_numbers_in_square(nb, g[0]-1, g[1]-1, 3)
        if len(ad_nos) == 2:
            res += ad_nos[0].no * ad_nos[1].no
        elif len(ad_nos) > 2:
            print("error too many gears found.")
    return res


if __name__ == "__main__":
    with open("../../inputs/day3/input", "r") as fid:
        inp_data = fid.read()
    symbols, numbers, gears = parse_input(inp_data)
    print("Solution1")
    print(solution1(symbols, numbers))
    print("Solution2")
    print(solution2(symbols, numbers, gears))


