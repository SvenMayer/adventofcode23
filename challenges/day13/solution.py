#!/usr/bin/python3
TEST_DATA1 = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.
"""

TEST_DATA2 = """#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""

TEST_DATA3 = """.##..##.#
.#.##.#..
#......##
#......##
.#.##.#..
.##..##..
.#.##.#.#
"""


def parse_field(field_str):
    field_str = field_str.strip()
    rows = []
    cols = []

    for i, r in enumerate(field_str.split("\n")):
        row = 0
        for j, c in enumerate(r):
            if i == 0:
                cols.append(0)
            if c == "#":
                row |= 1 << j
                cols[j] |= 1 << i
        rows.append(row)
    
    return rows, cols


def getlreftreflectionpt(inp):
    idx = [i for i in range(len(inp)) if inp[i] == inp[0]]
    if len(idx) > 1:
        if len(idx) % 2:
            idx = idx[:-1]
    splits = []
    for dl in idx[1:]:
        l = dl
        i = 0
        while i < l:
            if inp[i] != inp[l]:
                break
            l -= 1
            i += 1
        if l < i:
            splits.append((dl+1)//2)
    return splits


def getreflection(inp):
    splits = getlreftreflectionpt(inp)
    splits2 =  getlreftreflectionpt(inp[::-1])
    splits.extend([len(inp) - itm for itm in splits2])
    return splits


def reflection(data):
    rows, cols = parse_field(data)
    splitsh = getreflection(rows)
    splitsv = getreflection(cols)
    if len(splitsh) == 1 and len(splitsv) == 0:
        return "horizontal", splitsh[0]
    elif len(splitsv) == 1 and len(splitsh) == 0:
        return "vertical", splitsv[0]
    else:
        import pdb;pdb.set_trace()


def solution1(inp):
    res = 0
    for field_str in inp.split("\n\n"):
        direction, line = reflection(field_str)
        if direction == "vertical":
            res += line
        elif direction == "horizontal":
            res += 100 * line
        else:
            raise TypeError()
    return res


if __name__ == "__main__":
    with open("../../inputs/day13/input", "r") as fid:
        data = fid.read()

    print("Solution1")
    print(solution1(data))
