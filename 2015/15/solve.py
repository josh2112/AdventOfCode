"""https://adventofcode.com/2015/day/15"""

import argparse
import time
from itertools import product

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def parse(data: list[str]) -> tuple[str, tuple[int, ...]]:
    # Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
    for line in data:
        tk = line.replace(":", "").replace(",", "").split()
        yield tk[0], (int(tk[2]), int(tk[4]), int(tk[6]), int(tk[8]))


def score_cookie(
    ings: list[tuple[str, tuple[int, ...]]], amounts: tuple[int, ...]
) -> int:
    score = 1
    for p in range(len(ings[0][1])):
        s = max(sum(ing[1][p] * amounts[i] for i, ing in enumerate(ings)), 0)
        if s == 0:
            return 0
        score *= s
    return score


def prob_1(data: list[str]) -> int:
    ings = list(parse(data))
    max_score = 0
    for amts in (
        p for p in product(range(101), repeat=len(ings[0][1])) if sum(p) == 100
    ):
        score = score_cookie(ings, amts)
        print(f"{amts}: {score}")
        max_score = max(max_score, score)
    return max_score


def prob_2(data: list[str]) -> int:
    print(data)
    return 0


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2015 day 15.")
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
