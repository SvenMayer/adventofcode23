#!/usr/bin/python3

TEST_DATA = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""

def calc_load(data):
    len_row = len(data.split("\n")[0])
    cols = [data[i::len_row+1] for i in range(len_row)]
    len_col = len(cols[0])
    res = 0
    for c in cols:
        offset = 0
        for b in c.split("#"):
            for j in range(b.count("O")):
                res += len_col - (j + offset)
            offset += 1 + len(b)
    print(res)


if __name__ == "__main__":
    with open("../../inputs/day14/input", "r") as fid:
        data = fid.read()
    print(calc_load(data))