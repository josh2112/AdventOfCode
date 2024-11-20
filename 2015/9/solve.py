"""https://adventofcode.com/2015/day/9"""

import argparse
import time
from dataclasses import dataclass
from itertools import permutations
from sys import maxsize

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def parse(data: list[str]) -> tuple[tuple[str, str], int]:
    for line in data:
        tk = line.split()
        yield (tk[0][:2], tk[2][:2]), int(tk[4])
        yield (tk[2][:2], tk[0][:2]), int(tk[4])


def calc_dist(path: tuple[str, ...], edges: dict[tuple[str, str], int]) -> int:
    return sum(edges[hop] for hop in zip(path, path[1:]))


def prob_1(data: list[str]) -> int:
    edges = dict(parse(data))
    best = (None, maxsize)  # path, dist
    for path in permutations(set(v for pr in edges for v in pr)):
        dist = calc_dist(path, edges)
        if dist < best[1]:
            best = (path, dist)
    return best[1]


def prob_2(data: list[str]) -> int:
    edges = dict(parse(data))
    worst = (None, 0)  # path, dist
    for path in permutations(set(v for pr in edges for v in pr)):
        dist = calc_dist(path, edges)
        if dist > worst[1]:
            worst = (path, dist)
    return worst[1]


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2015 day 9.")
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
