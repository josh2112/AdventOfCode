"""https://adventofcode.com/2023/day/2"""

import argparse
import math
import re
import time

# Input file path, or None for the default, "input.txt"
INPUT = "input.txt"

# Daily problem to solve, 1 or 2
PART = 2


def parse(g):
    return (int(g[0].split()[1]), [r.split(", ") for r in g[1:]])


def process(data: list[str]):
    return [parse(re.split("[;:]", line)) for line in data]


def prob_1(data: list[str]):
    maxcol = {"red": 12, "green": 13, "blue": 14}

    def is_impossible(g):
        for rnd in g[1:]:
            for ballcnts in rnd:
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
        for rnd in g[1:]:
            for ballcnts in rnd:
                for ballcnt in ballcnts:
                    num, col = ballcnt.split()
                    if int(num) > max_balls_for_game[col]:
                        max_balls_for_game[col] = int(num)
        return math.prod(max_balls_for_game.values())

    return sum(power(g) for g in process(data))


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2023 day 2.")
    parser.add_argument("-p", "--part", choices=("1", "2", "all"), default=str(PART))
    parser.add_argument("-i", "--input", default=INPUT)
    args = parser.parse_args()
    part, infile = args.part, args.input

    with open(infile, mode="r", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    start = time.perf_counter()
    if part in ("1", "all"):
        print(f"Part 1: {prob_1(data)}")
    if part in ("2", "all"):
        print(f"Part 2: {prob_2(data)}")

    elapsed = time.perf_counter() - start
    print(f"Time: {elapsed} s")

    return elapsed


if __name__ == "__main__":
    main()
