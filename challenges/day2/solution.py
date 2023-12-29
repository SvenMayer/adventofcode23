#! /usr/bin/python3
MAX_RED_S1 = 12
MAX_GREEN_S1 = 13
MAX_BLUE_S1 = 14


class Game:
    def __init__(self, ln):
        self._parse_game(ln)

    def _parse_game(self, ln):
        game, draws = ln.split(":")
        _, no = game.split(" ")
        self.no = int(no.strip())
        self.draws = [self._parse_draw(itm) for itm in draws.split(";")]

    def _parse_draw(self, draw):
        res = {"red": 0, "green": 0, "blue": 0}
        for chunk in draw.split(","):
            chunk = chunk.strip()
            if len(chunk) == 0:
                continue
            no, color = chunk.split(" ")
            res[color] = int(no)
        return res

    def max_dice(self, color):
        return max([d[color] for d in self.draws])


def parse_games(inp):
    return [Game(ln) for ln in inp.split("\n") if len(ln.strip()) != 0]


def evaluate_solution_1(games):
    res = 0
    for g in games:
        if (g.max_dice("red") <= MAX_RED_S1
                and g.max_dice("green") <= MAX_GREEN_S1
                and g.max_dice("blue") <= MAX_BLUE_S1):
            res += g.no
    return res


def evaluate_solution_2(games):
    res = 0
    for g in games:
        res += g.max_dice("red") * g.max_dice("green") * g.max_dice("blue")
    return res


if __name__ == "__main__":
    with open("../../inputs/day2/input", "r") as fid:
        inp_data = fid.read()
    games = parse_games(inp_data)
    print("Solution1")
    print(evaluate_solution_1(games))
    print("Solution2")
    print(evaluate_solution_2(games))