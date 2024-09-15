#!/usr/bin/python3
import copy


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


class Range:
    def __init__(self, lBound, uBound):
        self.lBound = lBound
        self.uBound = uBound
    
    def split_gt(self, th):
        if self.lBound > th:
            return self, None
        elif self.uBound <= th:
            return None, self
        else:
            return Range(th + 1, self.uBound), Range(self.lBound, th), 
    
    def split_lt(self, th):
        if self.uBound < th:
            return self, None
        elif self.lBound >= th:
            return None, self
        else:
            return Range(self.lBound, th -1), Range(th, self.uBound)

    def split(self, operator, th):
        if operator == "<":
            return self.split_lt(th)
        else:
            return self.split_gt(th)
    
    def __len__(self):
        return self.uBound - self.lBound + 1


class MachinePart:
    def __init__(self):
        self.x = Range(1, 4000)
        self.m = Range(1, 4000)
        self.a = Range(1, 4000)
        self.s = Range(1, 4000)
    
    def split(self, itm, operator, th):
        l1, l2 = getattr(self, itm).split(operator, th)
        if l1 is None:
            setattr(self, itm, l2)
            return None, self
        elif l2 is None:
            setattr(self, itm, l1)
            return self, None
        else:
            r1 = copy.deepcopy(self)
            setattr(r1, itm, l1)
            setattr(self, itm, l2)
            return r1, self
        
    @property
    def value(self):
        return len(self.x) * len(self.m) * len(self.a) * len(self.s)


def parse_input(data):
    def workflow_parser(ln):
        name, inststr = ln.strip("}").split("{")
        chunks = inststr.split(",")
        inst = []
        for chk in chunks[:-1]:
            com_str = chk.split(":")
            inst.append((
                chk[0],
                ">" if ">" in chk else "<",
                int(com_str[0][2:]),
                com_str[1]
            ))
        return name, inst, chunks[-1] 
    parser = workflow_parser
    workflows = []
    for ln in data.split("\n"):
        if len(ln) == 0:
            return workflows
        workflows.append(parser(ln))


def handle_workflow(workflow, mpart):
    next_steps = []
    finish = []
    for inst in workflow[1]:
        mpass, mpart = mpart.split(inst[0], inst[1], inst[2])
        if mpass is not None:
            if inst[3] in "RA":
                finish.append((inst[3], mpass))
            else:
                next_steps.append((inst[3], mpass))
        if mpart is None:
            break
    if mpart is not None:
        if workflow[2] in "RA":
            finish.append((workflow[2], mpart))
        else:
            next_steps.append((workflow[2], mpart))
    return next_steps, finish


def solution2(data):
    workflows = parse_input(data)
    workflow_dict = dict([(itm[0], itm) for itm in workflows])
    next_steps = [("in", MachinePart())]
    finish = []
    while len(next_steps):
        wf_name, part = next_steps.pop(0)
        ns, fi = handle_workflow(workflow_dict[wf_name], part)
        next_steps.extend(ns)
        finish.extend(fi)
    res = 0
    for itm in finish:
        if itm[0] == "A":
            res += itm[1].value
    return res


print("Test")
print(solution2(TEST_DATA))

print("Solution 2")
with open("../../inputs/day19/input", "r") as fid:
    print(solution2(fid.read()))
