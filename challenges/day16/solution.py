#!/usr/bin/python3

TEST_DATA = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""


def get_field(data, idx, nc, nr):
    return data[idx[1]*(nc+1)+idx[0]]


def next_step(path, data, size, postocheck):
    pos = postocheck.pop(0)
    idx = pos[:2]
    direction = pos[2:]
    global tiles
    if (idx[0] >= size[0] or idx[0] < 0) or (idx[1] >= size[1] or idx[1] < 0):
        return
    if pos in path:
        return
    path.append(pos)
    f = get_field(data, idx, *size)
    if f == "." or (f == "-" and direction[1] == 0) or (f == "|" and direction[0] == 0):
        pos = idx[0] + direction[0], idx[1] + direction[1], direction[0], direction[1]
        postocheck.append(pos)
    elif f == "-":
        direction = 1, 0
        pos = idx[0] + direction[0], idx[1] + direction[1], direction[0], direction[1]
        postocheck.append(pos)
        direction = -1, 0
        pos = idx[0] + direction[0], idx[1] + direction[1], direction[0], direction[1]
        postocheck.append(pos)
    elif f == "|":
        direction = 0, 1
        pos = idx[0] + direction[0], idx[1] + direction[1], direction[0], direction[1]
        postocheck.append(pos)
        direction = 0, -1
        pos = idx[0] + direction[0], idx[1] + direction[1], direction[0], direction[1]
        postocheck.append(pos)
    elif f == "\\":
        direction = direction[1], direction[0]
        pos = idx[0] + direction[0], idx[1] + direction[1], direction[0], direction[1]
        postocheck.append(pos)
    elif f == "/":
        direction = -1 * direction[1], -1 * direction[0]
        pos = idx[0] + direction[0], idx[1] + direction[1], direction[0], direction[1]
        postocheck.append(pos)
    else:
        import pdb;pdb.set_trace()


def get_unique_tiles(path):
    return [itm for itm in set([p[:2] for p in path])]


def get_size(data):
    return len(data.split("\n")[0]), data.count("\n")


def solution1(data):
    pos = [(0, 0, 1, 0)]
    size = get_size(data)
    path = []
    while len(pos):
        next_step(path, data, size, pos)
    return len(get_unique_tiles(path))


def get_length_and_edges_touched(data, size, startpos):
    size = get_size(data)
    path = []
    pos = [startpos]
    while len(pos):
        next_step(path, data, size, pos)
    return len(get_unique_tiles(path)), [
        (itm[0], itm[1], -1*itm[2], -1*itm[3]) for itm in path
        if itm[0] == 0 or itm[0] == size[0] or itm[1] == 0 or itm[1] == size[1]]


def get_all_starting_pos(size):
    posT = [(i, 0, 0, 1) for i in range(size[0])]
    posR = [(0, i, 1, 0) for i in range(size[1])]
    posB = [(i, size[1], 0, -1) for i in range(size[0])]
    posL = [(size[0], i, -1, 0) for i in range(size[0])]
    return posT + posR + posB + posL


def solution2(data):
    size = get_size(data)
    tested_pos = []
    max_l = 0
    for pos in get_all_starting_pos(size):
        if pos in tested_pos:
            print("Skipping")
            continue
        l, eg = get_length_and_edges_touched(data, size, pos)
        tested_pos.append(pos)
        tested_pos.extend(eg)
        max_l = l if l > max_l else max_l
    return max_l


if __name__ == "__main__":
    with open("../../inputs/day16/input", "r") as fid:
        data = fid.read()
    print("Solution2")
    print(solution2(data))
