#! /usr/bin/python3

def parse_line1(ln):
    _, numbers = ln.split(":")
    return [int(itm) for itm in numbers.split(" ") if len(itm) > 0]


def parse_line2(ln):
    _, numbers = ln.split(":")
    return int(numbers.replace(" ", ""))


def parse_input1(inp):
    lntime, lndistance = inp.strip().split("\n")
    times = parse_line1(lntime)
    distances = parse_line1(lndistance)
    races = [itm for itm in zip(times, distances)]
    return races


def parse_input2(inp):
    lntime, lndistance = inp.strip().split("\n")
    time = parse_line2(lntime)
    distance = parse_line2(lndistance)
    race = (time, distance)
    return race


def solution1(races):
    # function of distance traveled over button press time
    # is a parabola. The zeros of that parabola shifted by
    # the minimum win distance plus one are the two press
    # times between which the boat travels farther than the
    # winning distance.
    res = 1
    for r in races:
        T, D = r
        p1 = (0.25 * T**2 - D - 1)**0.5
        zeros = -1 * p1 + 0.5 * T, p1 + 0.5 * T
        # Only integers valid for button press time.
        # You can only win with the integers that fall within the
        # caluclated range.
        lower = int(zeros[0] // 1 +1 if zeros[0] % 1 else zeros[0] // 1)
        upper = int(zeros[1])
        b = upper - lower + 1
        res *= b
    return res


def solution2(race):
    return solution1([race])


if __name__ == "__main__":
    with open("../../inputs/day6/input", "r") as fid:
        data = fid.read()
    races1 = parse_input1(data)
    print("Solution1")
    print(solution1(races1))
    race2 = parse_input2(data)
    print("Solution2")
    print(solution2(race2))