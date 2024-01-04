#!/usr/bin/python3
TEST_DATA = """
....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#.......
"""

PADDING = 999999

def expand_universe(inp):
    inp = inp.strip()
    empty_cols = [0,]
    len_row = inp.index("\n")
    for i in range(len_row):
        if "#" not in inp[i::len_row+1]:
            empty_cols.append(i)
    empty_cols.append(len_row)
    rows = []
    for row in inp.strip().split("\n"):
        r = ""
        for i in range(0, len(empty_cols)-1):
            r += row[empty_cols[i]:empty_cols[i+1]] + "."
        if row.count("#") == 0:
            rows.append(r)
        rows.append(r)
    return rows


def get_rows_and_cols_to_expand(inp):
    inp = inp.strip()
    empty_cols = []
    len_row = inp.index("\n")
    for i in range(len_row):
        if "#" not in inp[i::len_row+1]:
            empty_cols.append(i)
    empty_rows = []
    for i, row in enumerate(inp.strip().split("\n")):
        if row.count("#") == 0:
            empty_rows.append(i)
    return empty_rows, empty_cols


def number_galaxies(map):
    galaxies = []
    for i, row in enumerate(map):
        for j, c in enumerate(row):
            if c == "#":
                galaxies.append((j, i))
    return galaxies


def get_distance(xy0, xy1):
    return abs(xy0[0] - xy1[0]) + abs(xy0[1] - xy1[1])


def solution1(galaxies):
    res = 0
    for i in range(len(galaxies)):
        for j in range(i+1, len(galaxies)):
            res += get_distance(galaxies[i], galaxies[j])
    return res


def apply_expansion(galaxies, rows_to_expand, cols_to_expand):
    max_row = max([max([g[1] for g in galaxies]), max(rows_to_expand)]) + 1
    max_col = max([max([g[0] for g in galaxies]), max(cols_to_expand)]) + 1
    row_padding = max_row * [0]
    col_padding = max_col * [0]

    for r in rows_to_expand:
        row_padding[r:] = [itm + PADDING for itm in row_padding[r:]]
    for c in cols_to_expand:
        col_padding[c:] = [itm + PADDING for itm in col_padding[c:]]
    g_res = []
    for g in galaxies:
        x, y = g
        x += col_padding[x]
        y += row_padding[y]
        g_res.append((x, y))
    return g_res


def solution2(inp):
    galaxies = number_galaxies(inp.strip().split("\n"))
    r_to_expand, c_to_expand = get_rows_and_cols_to_expand(inp)
    extended = apply_expansion(galaxies, r_to_expand, c_to_expand)
    res = 0
    for i in range(len(extended)):
        for j in range(i+1, len(extended)):
            res += get_distance(extended[i], extended[j])
    return res


if __name__ == "__main__":
    # Test
    if False:
        expanded_universe = expand_universe(TEST_DATA)
        print("\n".join(expanded_universe))
        galaxies = number_galaxies(expanded_universe)
        print(galaxies)
        distance01 = get_distance(galaxies[0], galaxies[1])
        print(distance01)

    with open("../../inputs/day11/input", "r") as fid:
        data = fid.read()
    expand_universe = expand_universe(data)
    galaxies = number_galaxies(expand_universe)

    print("Solution1")
    print(solution1(galaxies))
    print("Solution2")
    print(solution2(data))
