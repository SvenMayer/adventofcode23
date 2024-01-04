#!/usr/bin/python3
MAP_AREA_TEST = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
"""


DIRS = {".": "", "7": "sw", "J": "nw", "|": "ns", "-": "ew", "L": "ne", "F": "se"}
INV_DIR = {"n": "s", "s": "n", "e" :"w", "w": "e"}
TURN = {"n": {"e": -1, "w": +1}, "e": {"s": -1, "n": +1},
        "s": {"w": -1, "e": +1}, "w": {"n": -1, "s": +1}}

class RingMap:
    def __init__(self, map):
        self.dirs = DIRS
        self.coords = (0, 0)
        self.map = map
        self.last_dir = ""
        self.initialize_map()

    def next_step(self):
        newdir = self.last_dir
        if newdir == "n":
            self.coords = (self.coords[0] - 1, self.coords[1])
        elif newdir == "s":
            self.coords = (self.coords[0] + 1, self.coords[1])
        elif newdir == "e":
            self.coords = (self.coords[0], self.coords[1] + 1)
        elif newdir == "w":
            self.coords = (self.coords[0], self.coords[1] - 1)
        row, col = self.coords
        possible_dir = self.dirs[self.map[row][col]]
        self.last_dir = possible_dir.strip(INV_DIR[newdir])
    
    @property
    def tile(self):
        return self.map[self.coords[0]][self.coords[1]]
    
    def initialize_map(self):
        for i, r in enumerate(self.map):
            if "S" in r:
                x, y = self.coords = (i, r.index("S"))
        initial_dirss = ""
        if x > 0 and "s" in DIRS[self.map[x-1][y]]:
            initial_dirss += "n"
        if x < len(self.map) - 1 and "n" in DIRS[self.map[x+1][y]]:
            initial_dirss += "s"
        if y > 0 and "e" in DIRS[self.map[x][y-1]]:
            initial_dirss += "w"
        if len(initial_dirss) == 1:
            initial_dirss += "e"
        self.dirs["S"] = initial_dirss
        self.last_dir = initial_dirss[0]
        self.initial_pos = x, y
        self.coords = x, y

    def go_to_start(self):
        self.initial_pos = self.coords
        self.last_dir = self.dirs["S"][0]
    
    @property
    def ring_length(self):
        self.go_to_start()
        self.next_step()
        ctr = 1
        while self.tile != "S":
            self.next_step()
            ctr += 1
        return ctr

    
    @property
    def ring_direction(self):
        self.go_to_start()
        dir0 = self.last_dir
        self.next_step()
        if dir0 == self.last_dir:
            turn = 0
        else:
            turn = TURN[dir0][self.last_dir]
        while self.tile != "S":
            dir0 = self.last_dir
            self.next_step()
            if dir0 == self.last_dir:
                continue
            turn += TURN[dir0][self.last_dir]
        return turn

    @property 
    def ring_area(self):
        if (self.ring_direction < 0):
            self.go_to_start()
            self.last_dir = self.dirs["S"][1]
        else:
            self.go_to_start()
        x0, y0 = self.coords
        self.next_step()
        x1, y1 = self.coords
        res = x0 * y1 - x1 * y0
        while self.tile != "S":
            x0, y0 = self.coords
            self.next_step()
            x1, y1 = self.coords
            res += x0 * y1 - x1 * y0
        res = (res - self.ring_length) // 2 + 1
        return res


def read_input(inp):
    return RingMap(inp.strip().split("\n"))


if __name__ == "__main__":
    with open("../../inputs/day10/input", "r") as fid:
        data = fid.read()
    rm = read_input(data)
    print("Solution1")
    print(rm.ring_length//2)
    print("Solution2")
    rmtest = RingMap(MAP_AREA_TEST.strip().split("\n"))
    print(rm.ring_area)