#!/usr/bin/python3

PRIMES_100 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59,
              61, 67, 71, 73, 79, 83, 89, 97]

TEST_INPUT = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""


class Node:
    def __init__(self, name):
        self.left = None
        self.right = None
        self.name = name

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        return self.name == other.name
    
    def __neq__(self, other):
        return not self.__eq(other)

    @property
    def R(self):
        return self.right

    @property
    def L(self):
        return self.left


def create_node_list(inp):
    node_list = []
    for ln in inp.strip().split("\n"):
        name, _ = ln.split("=")
        node_list.append(Node(name.strip()))
    return node_list


def link_node_list(node_list, inp):
    for ln in inp.strip().split("\n"):
        name, neighbors = ln.split("=")
        name = name.strip()
        l, r = neighbors.strip("() ").split(",")
        lnode = node_list[node_list.index(l.strip())]
        rnode = node_list[node_list.index(r.strip())]
        active_node = node_list[node_list.index(name)]
        active_node.left = lnode
        active_node.right = rnode


def parse_input(inp):
    idx_l1 = inp.index("\n")
    instructions = inp[:idx_l1]

    node_input = inp[idx_l1:].strip()
    node_list = create_node_list(node_input)
    link_node_list(node_list, node_input)

    return instructions, node_list


def get_nodes_ending_in_a(node_list):
    return [node for node in node_list if node.name[-1] == "A"]


def get_number_of_reps_to_node_ending_in_z(instructions, node_list):
    res = []
    for n in node_list:
        node = n
        ctr = 0
        while node.name[-1] != "Z":
            for inst in instructions:
                node = getattr(node, inst)
            ctr += 1
        res.append(ctr)
    return res


def get_prime_factors(number):
    res = []
    while number > 1:
        for p in PRIMES_100:
            if number % p == 0:
                res.append(p)
                number = number // p
                break
    return res


def get_lcm(number_list):
    prime_factors = [get_prime_factors(n) for n in number_list]
    common_primes = [max([pf.count(p) for pf in prime_factors])
                     for p in PRIMES_100]
    res = 1
    for no, p in zip(common_primes, PRIMES_100):
        if no:
            res *= no * p
    return res


def solution1(instructions, node_list):
    node = node_list[node_list.index("AAA")]
    ctr = 0
    while (node != "ZZZ"):
        for inst in instructions:
            node = getattr(node, inst)
            ctr += 1
    return ctr


def solution2(instructions, node_list):
    anodes = get_nodes_ending_in_a(node_list)
    nreps = get_number_of_reps_to_node_ending_in_z(instructions, anodes)
    lcm_reps = get_lcm(nreps)
    return lcm_reps*len(instructions)

if __name__ == "__main__":
    test_inst, testaaanode = parse_input(TEST_INPUT)
    print("Test Solution")
    print(solution1(test_inst, testaaanode))
    with open("../../inputs/day8/input", "r") as fid:
        data = fid.read()
    instructions, node_list = parse_input(data)
    print("Solution1")
    print(solution1(instructions, node_list))
    print("Solution2")
    print(solution2(instructions, node_list))
    