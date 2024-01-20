#!/usr/bin/python3
TEST_DATA = b"rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"


class Lens:
    def __init__(self, name, focal):
        self.name = name
        self.focal = focal
    
    def __eq__(self, other):
        return self.name == other.name

    def __neq__(self, other):
        return self != other


def hash_digest(str):
    state = 0
    for c in str:
        state += c
        state *= 17
        state %= 256
    return state


def parse_instruction(instr):
    if b"-" in instr:
        return instr[:-1], b"-", None
    name, focal = instr.split(b"=")
    return name, b"=", int(focal)


def solution1(data):
    res = 0
    for itm in data.split(b","):
        res += hash_digest(itm)
    return res


def fillboxes(data):
    boxes = [[] for i in range(256)]
    for instr_str in data.split(b","):
        name, instr, focal = parse_instruction(instr_str)
        boxno = hash_digest(name)
        l = Lens(name, focal)
        if instr == b"-":
            try:
                idx = boxes[boxno].index(l)
            except ValueError:
                continue
            boxes[boxno].pop(idx)
        else:
            try:
                idx = boxes[boxno].index(l)
                boxes[boxno][idx] = l
            except ValueError:
                boxes[boxno].append(l)
    return boxes

def solution2(data):
    boxes = fillboxes(data)
    res = 0
    for i, b in enumerate(boxes):
        for j, l in enumerate(b):
            res += (i + 1) * (j + 1) * l.focal
    return res
        


if __name__ == "__main__2":
    res = 0
    for itm in TEST_DATA.split(b","):
        res += hash_digest(itm)
        print(str(itm) + ": " + str(hash_digest(itm)))
    print(res)


if __name__ == "__main__":
    with open("../../inputs/day15/input", "rb") as fid:
        data = fid.read().strip()
    print("Solution 1")
    print(solution1(data))
    print("Solution2")
    print(solution2(data))

