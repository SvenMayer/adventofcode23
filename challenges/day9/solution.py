#!/usr/bin/python3
import numpy as np


def read_input(inp):
    res = []
    for ln in inp.strip().split("\n"):
        res.append(np.fromstring(ln, sep=" ", dtype=int))
    return res


def get_derivatives(data):
    res = []
    d = data
    while np.max(d) != 0 or np.min(d) != 0:
        d = np.diff(d)
        res.append(d)
    return res


def next_value(data):
    derivatives = get_derivatives(data)
    last_element = np.r_[[data[-1]], [d[-1] for d in derivatives]][::-1]
    return np.sum(last_element)


def previous_value(data):
    # Rather than adding the derivative has to be substracted.
    # Since (-1) (-1) = (1) only every other element has to be substracted.
    # v_k-1 = v_k - d1_k-1
    # d1_k-1 = d1_k - d2_k-1
    # d2_k-2 = d2_k - d3_k-1
    # ...
    # => v_k-1 = v_k - d1_k + d2_k - d3_k + ...
    derivatives = get_derivatives(data)
    first_derivative = np.r_[[data[0]], [d[0] for d in derivatives]]
    first_derivative[1::2] *= -1
    return np.sum(first_derivative[::-1])


def solution1(full_data):
    res = 0
    for row in full_data:
        res += next_value(row)
    return res


def solution2(full_data):
    res = 0
    for row in full_data:
        res += previous_value(row)
    return res


if __name__ == "__main__":
    with open("../../inputs/day9/input", "r") as fid:
        data = fid.read()
    parsed_data = read_input(data)
    print("Solution1")
    print(solution1(parsed_data))
    print("Solution2")
    print(solution2(parsed_data))
