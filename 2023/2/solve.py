#!/usr/bin/env python3
import math
import re

# Input file path, or None for the default, "input.txt"
INPUT = "input.txt"

# Daily problem to solve, 1 or 2
PROBLEM = 2


def process(data: list[str]):
    process = lambda g: (int(g[0].split()[1]), [r.split(", ") for r in g[1:]])
    return [process(re.split("[;:]", line)) for line in data]


def prob_1(data: list[str]):
    maxcol = {"red": 12, "green": 13, "blue": 14}

    def is_impossible(g):
        for round in g[1:]:
            for ballcnts in round:
                for ballcnt in ballcnts:
                    num, col = ballcnt.split()
                    if int(num) > maxcol[col]:
                        return True
        return False

    games = process(data)
    return sum(int(g[0]) for g in games if not is_impossible(g))


def prob_2(data: list[str]):
    def power(g):
        max_balls_for_game = {"red": 0, "green": 0, "blue": 0}
        for round in g[1:]:
            for ballcnts in round:
                for ballcnt in ballcnts:
                    num, col = ballcnt.split()
                    if int(num) > max_balls_for_game[col]:
                        max_balls_for_game[col] = int(num)
        return math.prod(max_balls_for_game.values())

    return sum(power(g) for g in process(data))


def main():
    with open(INPUT or "input.txt", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    print(f"Problem {PROBLEM}")
    print(prob_1(data) if PROBLEM == 1 else prob_2(data))


if __name__ == "__main__":
    main()
