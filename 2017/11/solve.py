"""https://adventofcode.com/2017/day/11"""

import argparse
import time
from functools import reduce

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1

DIRS = {
    "n": (0, 1, -1),
    "ne": (1, 0, -1),
    "se": (1, -1, 0),
    "s": (0, -1, 1),
    "sw": (-1, 0, 1),
    "nw": (-1, 1, 0),
}


def add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def dist(p):
    return max(abs(c) for c in p)


def prob_1(data: list[str]) -> int:
    return dist(reduce(add, [DIRS[d] for d in data[0].split(",")]))


def prob_2(data: list[str]) -> int:
    p, maxdist = (0, 0, 0), 0

    for i in data[0].split(","):
        p = add(p, DIRS[i])
        if (d := dist(p)) > maxdist:
            maxdist = d
    return maxdist


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solves AoC 2017 day 11.")
    parser.add_argument("-p", "--part", choices=("1", "2", "all"), default=str(PART))
    parser.add_argument("-i", "--input", default=INPUT)
    args = parser.parse_args()

    with open(args.input, mode="r", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    start = time.perf_counter()
    if args.part in ("1", "all"):
        print(f"Part 1: {prob_1(data)}")
    if args.part in ("2", "all"):
        print(f"Part 2: {prob_2(data)}")

    print(f"Time: {time.perf_counter() - start} s")
