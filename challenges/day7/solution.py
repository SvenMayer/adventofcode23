#! /usr/bin/python3

CARDS1 = "AKQJT98765432"
CARDVALUES1 = dict([(c, i) for i, c in enumerate(CARDS1[::-1])])
CARDS2 = "AKQT98765432J"
CARDVALUES2 = dict([(c, i) for i, c in enumerate(CARDS2[::-1])])


class Hand:
    def __init__(self, hand_str):
        self.value = self._get_full_hand_classification(hand_str)
    
    @staticmethod
    def _get_hand_type(hand_str):
        raise NotImplemented()

    def _get_full_hand_classification(self, hand_str):
        return (
            self._get_hand_type(hand_str),
            self.CARDVALUES[hand_str[0]],
            self.CARDVALUES[hand_str[1]],
            self.CARDVALUES[hand_str[2]],
            self.CARDVALUES[hand_str[3]],
            self.CARDVALUES[hand_str[4]]
        )

    def __gt__(self, other):
        return self.value > other.value

    def __lt__(self, other):
        return self.value < other.value
    
    def __eq__(self, other):
        return self.value == other.value
    
    def __ge__(self, other):
        return self.value >= other.value
    
    def __le__(self, other):
        return self.value <= other.value
    
    def __ne__(self, other):
        return self.value != other.value


class Hand1(Hand):
    def __init__(self, *args, **kwargs):
        self.CARDVALUES = CARDVALUES1
        Hand.__init__(self, *args, **kwargs)

    @staticmethod
    def _get_hand_type(hand_str):
        char_counted = ""
        count = []
        for c in hand_str:
            if c in char_counted:
                continue
            count.append(hand_str.count(c))
            char_counted += c
        count.sort(reverse=True)
        hand_type = None
        if count[0] == 5:
            hand_type = 6
        elif count[0] == 4:
            hand_type = 5
        elif count[0] == 3 and count[1] == 2:
            hand_type = 4
        elif count[0] == 3:
            hand_type = 3
        elif count[0] == 2 and count[1] == 2:
            hand_type = 2
        elif count[0] == 2:
            hand_type = 1
        else:
            hand_type = 0
        return hand_type


class Hand2(Hand):
    def __init__(self, *args, **kwargs):
        self.CARDVALUES = CARDVALUES2
        Hand.__init__(self, *args, **kwargs)

    @staticmethod
    def _get_hand_type(hand_str):
        jcount = hand_str.count("J")
        char_counted = "J"
        count = []
        for c in hand_str:
            if c in char_counted:
                continue
            count.append(hand_str.count(c))
            char_counted += c
        count.sort(reverse=True)
        hand_type = None
        if (jcount == 5) or ((count[0] + jcount) == 5):
            hand_type = 6
        elif (count[0] + jcount) == 4:
            hand_type = 5
        elif len(count) == 2:
            hand_type = 4
        elif (count[0] + jcount) == 3:
            hand_type = 3
        elif len(count) == 3:
            hand_type = 2
        elif (count[0] + jcount) == 2:
            hand_type = 1
        else:
            hand_type = 0
        return hand_type


def parse_input1(inp):
    game = []
    for ln in inp.strip().split("\n"):
        hand_str, bet = ln.split(" ")
        game.append((Hand1(hand_str), int(bet)))
    return game


def parse_input2(inp):
    game = []
    for ln in inp.strip().split("\n"):
        hand_str, bet = ln.split(" ")
        game.append((Hand2(hand_str), int(bet)))
    return game


def solution(games):
    games.sort()
    res = 0
    for i, g in enumerate(games):
        res += (i + 1) * g[1]
    return res


if __name__ == "__main__":
    with open("../../inputs/day7/input", "r") as fid:
        data = fid.read()
    games1 = parse_input1(data)
    print("Solution 1")
    print(solution(games1))
    games2 = parse_input2(data)
    print("Solution 2")
    print(solution(games2))
