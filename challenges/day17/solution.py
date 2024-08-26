#!/usr/bin/python3
import heapq

TEST_DATA = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""

def get_penalty(node, board):
    return board[node[0]][node[1]]


def exists(n, sz):
    x, y, dx, dy, ct = n
    if (x < sz[0]) or (y < sz[1]) or (x > sz[2]) or (y > sz[3]):
        return False
    return True


def isend(n, sz, mins):
    if n[4] < mins:
        return False
    return n[0] == sz[2] and n[1] == sz[3]


def get_next_nodes(node, sz, mins=1, maxs=3):
    x, y, dx, dy, count = node
    nodes_ = []
    if count < maxs:
        x_ = x + dx
        y_ = y + dy
        n = x_, y_, dx, dy, count+1
        if exists(n, sz):
            nodes_.append(n)
    if count >= mins:
        x_ = x + dy
        y_ = y - dx
        n = x_, y_, dy, -dx, 1
        if exists(n, sz):
            nodes_.append(n)
        x_ = x - dy
        y_ = y + dx
        n = x_, y_, -dy, dx, 1
        if exists(n, sz):
            nodes_.append(n)
    return nodes_


def initialize_priority_queue(pq, board):
    n1 = (1, 0, 1, 0, 1)
    p1 = get_penalty(n1, board)
    n2 = (0, 1, 0, 1, 1)
    p2 = get_penalty(n2, board)
    pq.append((p1, n1))
    pq.append((p2, n2))
    pq.sort()


def get_path(fq, nlast):
    path = [nlast]
    l1, l2, l3 = zip(*fq)
    n = nlast
    while (n[0] != 0) or (n[1] != 0):
        try:
            idx = l2.index(n)
        except ValueError:
            import pdb;pdb.set_trace()
        n = l3[idx]
        path.append(n)
    return path


def parse_board(brd_str):
    return [[int(letter) for letter in row] for row in brd_str.split("\n")[:-1]]


def solve(brd_str, mins=1, maxs=3):
    board = parse_board(brd_str)
    PRIORITY_QUEUE = []
    SZ = 0, 0, len(board)-1, len(board[0])-1

    initialize_priority_queue(PRIORITY_QUEUE, board)
    FINISHED_QUEUE = set([
        (1, 0, 1, 0, 1),
        (0, 1, 0, 1, 1)
    ])
    
    final_penalty = 0
    while True:
        p, n = heapq.heappop(PRIORITY_QUEUE)
        if isend(n, SZ, mins):
            final_penalty = p
            break
        for n_ in get_next_nodes(n, SZ, mins, maxs):
            if n_ in FINISHED_QUEUE:
                continue
            p_ = get_penalty(n_, board)
            heapq.heappush(PRIORITY_QUEUE, (p + p_, n_))
            FINISHED_QUEUE.add(n_)
        PRIORITY_QUEUE.sort()

    return final_penalty


penalty = solve(TEST_DATA)

print("Test Data")
print(penalty)

print("Solution 1")
with open("../../inputs/day17/input", "r") as fid:
    data = fid.read()
penalty = solve(data)
print(penalty)

print("Solution 2")
penalty = solve(data, 4, 10)
print(penalty)