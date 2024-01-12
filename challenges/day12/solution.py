#!/usr/bin/python3
import functools

TEST_DATA = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""


@functools.lru_cache(maxsize=None)
def get_count(instr, solution):
    instr = instr.lstrip(".")
    if len(solution) == 0:
        if "#" not in instr:
            return 1
        else:
            return 0
    if len(instr) <= solution[0]:
        return 0
    if instr[0] == "#":
        if "." in instr[:solution[0]] or instr[solution[0]] == "#":
            return 0
    res = 0
    if instr[0] == "?": 
        dot_str = instr[1:].lstrip(".")
        res += get_count(dot_str, solution)
    if "." not in instr[:solution[0]] and instr[solution[0]] != "#":
        pound_str = instr[solution[0]+1:].lstrip(".")
        pound_solution = tuple(solution[1:])
        res += get_count(pound_str, pound_solution)
    return res


def parse_input(inp):
    res = []
    for ln in inp.strip().split("\n"):
        springs, meta = ln.split(" ")
        solution = [int(itm) for itm in meta.split(",")]
        res.append((springs, solution))
    return res


def unfold_input(inp):
    res = []
    for springs, solution in inp:
        res.append(("?".join(5*[springs]), 5*solution))
    return res


def solution1(inp):
    global FULLSTR, BASESOLUTION, fullstr_list
    res = 0
    data = parse_input(inp)
    for itm in data:
        restmp = get_count(itm[0] + ".", tuple(itm[1]))
        res += restmp
    return res


def solution2(inp):
    res = 0
    data = parse_input(inp)
    data = unfold_input(data)
    for i, itm in enumerate(data):
        ln, data = itm
        ln = ln + "."
        data = tuple(data)
        restmp = get_count(ln, data)
        res += restmp
    return res



if __name__ == "__main__":
    if False:
        inp = parse_input(TEST_DATA)
        for itm in inp:
            print(get_number_of_matches(itm[0], itm[1]))
    with open("../../inputs/day12/input", "r") as fid:
        data = fid.read()
    print("Solution1")
    print(solution1(data))
    print("Solution2")
    print(solution2(data))