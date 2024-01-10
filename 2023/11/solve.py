"""https://adventofcode.com/2023/day/11"""

import argparse
import time
from itertools import combinations

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 2


def expand_and_calc_dist(data: list[str], expansion: int):
    stars = [
        (x, y)
        for y, row in enumerate(data)
        for x, c in enumerate(row)
        if "#" in row
        if c == "#"
    ]
    for y in sorted(
        list(set(range(len(data))).difference(y for _, y in stars)), reverse=True
    ):
        for i, s in enumerate(stars):
            if s[1] > y:
                stars[i] = (s[0], s[1] + expansion)
    for x in sorted(
        list(set(range(len(data[0]))).difference(x for x, _ in stars)), reverse=True
    ):
        for i, s in enumerate(stars):
            if s[0] > x:
                stars[i] = (s[0] + expansion, s[1])

    dist = 0
    for c in combinations(stars, 2):
        dist += abs(c[0][0] - c[1][0]) + abs(c[0][1] - c[1][1])
    return dist


def prob_1(data: list[str]):
    return expand_and_calc_dist(data, 1)


def prob_2(data: list[str]):
    return expand_and_calc_dist(data, 999999)


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2023 day 11.")
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
