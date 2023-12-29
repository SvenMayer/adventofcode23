#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 22:24:25 2023

@author: sven
"""
NUMBERS_ALL = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
               "seven": 7, "eight": 8, "nine": 9, "zero": 0, "1": 1, "2": 2,
               "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "0": 0}
NUMBERS_ONLY_NUMERIC= {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7,
                       "8": 8, "9": 9, "0": 0}

def number_at_idx_or_none(ln, idx, _NUMBERS_DICT):
    for spelled_number in _NUMBERS_DICT.keys():
        if ln[idx:].startswith(spelled_number):
            return _NUMBERS_DICT[spelled_number]
    return None


def get_first_number(ln, _NUMBERS_DICT):
    for i in range(len(ln)):
        first_number_or_none = number_at_idx_or_none(ln, i, _NUMBERS_DICT)
        if first_number_or_none is not None:
            return first_number_or_none


def get_last_number(ln, _NUMBERS_DICT):
    for i in range(len(ln)-1, -1, -1):
        last_number_or_none = number_at_idx_or_none(ln, i, _NUMBERS_DICT)
        if last_number_or_none is not None:
            return last_number_or_none


def get_code_for_line(ln, _NUMBERS_DICT):
    first = get_first_number(ln, _NUMBERS_DICT)
    last = get_last_number(ln, _NUMBERS_DICT)
    if first is None:
        import pdb;pdb.set_trace()
    return first * 10 + last


def get_solution(input, _NUMBERS_DICT):
    solution = 0
    for ln in input.split("\n"):
        ln = ln.strip()
        if len(ln) == 0:
            continue
        solution += get_code_for_line(ln, _NUMBERS_DICT)
    return solution


with open("../../inputs/day1/input", "r") as fid:
    data = fid.read()

print("Solution 1")
print(get_solution(data, NUMBERS_ONLY_NUMERIC))
print("Solution 2")
print(get_solution(data, NUMBERS_ALL))
