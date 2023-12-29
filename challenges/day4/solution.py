#! /usr/bin/python3

class Card:
    def __init__(self, ln):
        self._parse_card(ln)

    def _parse_card(self, ln):
        left, right = ln.split(":")
        self.no = int(left.replace(" ", "")[4:])
        winning_str, my_str = right.split("|")
        self.winning_numbers = self._parse_numbers(winning_str.strip())
        self.my_numbers = self._parse_numbers(my_str.strip())

    @staticmethod
    def _parse_numbers(number_str):
        return [int(itm) for itm in number_str.split(" ") if len(itm)]

    @property
    def value(self):
        count = self.no_matches
        if count == 0:
            return count
        return 2**(count - 1)

    @property
    def no_matches(self):
        return len([
            no for no in self.winning_numbers if no in self.my_numbers])


def parse_input(inp):
    cards = []
    for ln in inp.split("\n"):
        if len(ln.strip()) == 0:
            continue
        cards.append(Card(ln))
    return cards


def solution1(cards):
    res = 0
    for c in cards:
        res += c.value
    return res


def solution2(cards):
    totalcount = len(cards)
    count = len(cards) * [1]
    for i, c in enumerate(cards):
        wincount = c.no_matches
        idx1 = i+1
        idx2 = idx1 + wincount if idx1 + wincount < len(cards) else len(cards)
        count[idx1:idx2] = [itm + count[i] for itm in count[idx1:idx2]]
        totalcount += wincount * count[i]
    return totalcount


if __name__ == "__main__":
    with open("../../inputs/day4/input", "r") as fid:
        data = fid.read()
    cards = parse_input(data)
    print("Solution1")
    print(solution1(cards))
    print("Solution2")
    print(solution2(cards))