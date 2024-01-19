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
#OO..#...."""


N_REV = 1000000000


def calc_load(data):
    nr = data.count("\n") + 1
    res = 0
    for i, row in enumerate(data.split("\n")):
        res += (nr - i) * row.count("O")
    return res


def count_rows_and_cols(data):
    nr = data.count("\n") + 1
    nc = len(data.split("\n")[0])
    return nr, nc


def turn_right_and_tilt(nr, nc, data):
    cols = [data[i::nc+1] for i in range(nc)]
    blocks = [c[::-1].split("#") for c in cols]
    res = "\n".join(["#".join([b.count(".") * "." + b.count("O") * "O" for b in ln]) for ln in blocks])
    return nc, nr, res


def cycle_board(nr, nc, data):
    for i in range(4):
        nr, nc, data = turn_right_and_tilt(nr, nc, data)
    return nr, nc, data


def turn_left(nr, nc, data):
    cols = [data[i::nc+1] for i in range(nc)]
    return "\n".join(c[::-1] for c in cols)


def find_repeating_pattern(nr, nc, data):
    instances = dict()
    count = 0
    for i in range(N_REV):
        k = hash(data)
        if k in instances:
            idx0 = instances[k]
            idx1 = i
            count += 1
            if count == 10:
                return nr, nc, data, idx1, idx1-idx0
        instances[k] = i
        nr, nc, data = cycle_board(nr, nc, data)
    return nr, nc, data, N_REV, 0


def solution2(data):
    nr, nc = count_rows_and_cols(data)
    nr, nc, data, idx, period = find_repeating_pattern(nc, nc, data)
    steps_to_go = (N_REV - idx) % period
    for i in range(steps_to_go):
        nr, nc, data = cycle_board(nr, nc, data)
    return calc_load(data)


if __name__ == "__main__2":
    data = TEST_DATA
    nr = nc = 10
    print(data)
    print("")
    for i in range(3):
        nr, nc, data = cycle_board(nr, nc, data)
        print(data)
        print("")


if __name__ == "__main__":
    with open("../../inputs/day14/input", "r") as fid:
        data = fid.read().strip()
    print(solution2(data))
