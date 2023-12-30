#! /usr/bin/python3

class MapTable:
    def __init__(self, inp):
        # table
        # DEST_RANGE, SOURCE_RANGE, LENGTH
        self._parse_input(inp)
        self._fill_range()

    def _parse_input(self, inp):
        self.table = []
        for i, ln in enumerate(inp.split("\n")):
            if i == 0:
                self._parse_input_and_output_commodity(ln)
                continue
            dst_rg, src_rg, ln = ln.strip().split(" ")
            self.table.append((int(src_rg), int(dst_rg), int(ln)))
        self.table.sort()

    def _parse_input_and_output_commodity(self, ln):
        description, _ = ln.strip().split(" ")
        inco, outco = description.split("-to-")
        self.input_com = inco
        self.output_com = outco

    def _fill_range(self):
        x0 = 0
        additional_entries = []
        for entry in self.table:
            if entry[0] > x0:
                additional_entries.append((x0, x0, entry[0]-x0))
            x0 = entry[0] + entry[2]
        self.table.extend(additional_entries)
        self.table.sort()
        if (self.table[-1][0]+self.table[-1][2]) < 2**32:
            self.table.append((x0, x0, 2**32-x0))
        
    def get_dst_for_src(self, src):
        for mp in self.table:
            if src >= mp[0] and src < mp[0] + mp[2]:
                return mp[1] + src - mp[0]
    
    def map_multiple_ranges(self, srcs):
        rgs = []
        for src in srcs:
            ranges = self.map_range(src)
            rgs.extend(ranges)
        rgs.sort()
        return rgs

    def map_range(self, src):
        x0, ln = src
        ranges = []
        x0orig = x0
        lnorig = ln
        idx = 0
        for i, entry in enumerate(self.table):
            if x0 >= entry[0] and x0 < entry[0] + entry[2]:
                idx = i
                break
        while (ln > 0):
            entry = self.table[idx]
            l = entry[0] + entry[2] - x0
            if l > ln:
                l = ln
            ln = ln - l
            y0 = entry[1] + x0 - entry[0]
            ranges.append((y0, l))
            x0 += l
            idx += 1
        return ranges
            

def get_map_by_input(maps, input):
    for m in maps:
        if m.input_com == input:
            return m
    raise ValueError(f"Input '{input:s}' not in maps.")


def parse_seed_line(ln):
    _, keys = ln.split(":")
    return [int(itm) for itm in keys.strip().split(" ")]


def parse_input(inp):
    idx_ln1 = inp.index("\n")
    seeds = parse_seed_line(inp[:idx_ln1])
    maps = [MapTable(chk) for chk in inp[idx_ln1:].strip().split("\n\n")
            if len(chk)]
    return seeds, maps


def get_location_for_seed(maps, seed):
    com = "seed"
    addr = seed
    while com != "location":
        m = get_map_by_input(maps, com)
        com = m.output_com
        addr = m.get_dst_for_src(addr)
    return addr


def get_location_range_for_seed_range(maps, seed_range):
    com = "seed"
    addr = [seed_range]
    while com != "location":
        m = get_map_by_input(maps, com)
        com = m.output_com
        addr = m.map_multiple_ranges(addr)
    return addr


def solution1(seeds, maps):
    locations = []
    for s in seeds:
        locations.append(get_location_for_seed(maps, s))
    locations.sort()
    return locations[0]


def solution2(seeds, maps):
    locations = []
    for i, s in enumerate((itm for itm in zip(seeds[::2], seeds[1::2]))):
        locations.extend(get_location_range_for_seed_range(maps, s))
    locations.sort()
    return locations[0][0]


if __name__ == "__main__":
    with open("../../inputs/day5/input", "r") as fid:
        data = fid.read()
    seeds, maps = parse_input(data)
    print("Solution1")
    print(solution1(seeds, maps))
    print("Solution2")
    print(solution2(seeds, maps))