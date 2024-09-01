#!/usr/bin/python3

TEST_DATA = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""



def parse_input(data):
    def workflow_parser(ln):
        name, inststr = ln.strip("}").split("{")
        chunks = inststr.split(",")
        inst = []
        for chk in chunks[:-1]:
            com_str = chk.split(":")
            inst.append((
                chk[0],
                int.__gt__ if ">" in chk else int.__lt__,
                int(com_str[0][2:]),
                com_str[1]
            ))
        return name, inst, chunks[-1] 
    def toy_parser(ln):
        return dict([(itm[0], int(itm[2:])) for itm in ln.strip("{}").split(",")])
    parser = workflow_parser
    workflows = []
    toys = []
    reslist = workflows
    for ln in data.split("\n"):
        if len(ln) == 0:
            parser = toy_parser
            reslist = toys
            continue
        reslist.append(parser(ln))
    return workflows, toys


def apply_workflow(wf, part):
    for inst in wf[1]:
        if inst[1](part[inst[0]], inst[2]):
            return inst[3]
    return wf[2]


def process_parts(wf_dict, part):
    next_wf = "in"
    while next_wf not in ("A", "R"):
        next_wf = apply_workflow(wf_dict[next_wf], part)
    return next_wf


def solution1(data):
    workflows, mparts = parse_input(data)
    wf_dict = dict([(itm[0], itm) for itm in workflows])
    res = 0
    for p in mparts:
        if process_parts(wf_dict, p) == "A":
            res += p["x"] + p["m"] + p["a"] + p["s"]
    return res


print("Test Data")
print(solution1(TEST_DATA))

print("Solution 1")
with open("../../inputs/day19/input", "r") as fid:
    data = fid.read()
print(solution1(data))