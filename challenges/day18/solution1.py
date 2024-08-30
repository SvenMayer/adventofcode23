#!/usr/bin/python3

TEST_DATA = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""

def parse_line_solution1(ln):
    dir, nstp, color = ln.split(" ")
    return dir, nstp, color


def parse_line_solution2(ln):
    _, __ , hex = ln.split(" ")
    hex = hex[1:-1]
    nstp = int(hex[1:6], 16)
    dir = ["R", "D", "L", "U"][int(hex[6], 16)]
    return dir, nstp, hex


def parse_board(inp, lineparser=parse_line_solution1):
    def step(p0, dir, nstps):
        if dir == "D":
            return p0[0], p0[1] - nstps
        elif dir == "U":
            return p0[0], p0[1] + nstps
        elif dir == "L":
            return p0[0] - nstps, p0[1]
        elif dir == "R":
            return p0[0] + nstps, p0[1]
        
    trench = []
    pos = (0, 0)
    for i, ln in  enumerate(inp.split("\n")):
        if len(ln) == 0:
            continue
        dir, nstp, color = lineparser(ln)
        nstp = int(nstp)
#        if i == 0:
#            nstp += 1
        newpos = step(pos, dir, nstp)
        trench.append((pos, newpos, color[1:-1]))
        pos = newpos
    trench[-1] = trench[-1][0], (0, 0), trench[-1][2]

    return trench



def get_area(trench):
    A = 0
    l = 0
    for ln in trench:
        (x0, y0), (x1, y1), color = ln
        A += (x1 - x0) * y0 + 0.5 * abs(y0 - y1) + 0.5 * abs(x0 - x1)
    return int(A + 1)


print("Test Data")
trench = parse_board(TEST_DATA)
print(get_area(trench))

print("Solution 1")
with open("../../inputs/day18/input", "r") as fid:
    trench = parse_board(fid.read())
print(get_area(trench))

print("Test Data Solution 2")
trench = parse_board(TEST_DATA, parse_line_solution2)
print(get_area(trench))

print("Solution 2")
with open("../../inputs/day18/input", "r") as fid:
    trench = parse_board(fid.read(), parse_line_solution2)
print(get_area(trench))