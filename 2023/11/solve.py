#!/usr/bin/env python3

import time
from itertools import combinations

# https://adventofcode.com/2023/day/11

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
        for i in range(len(stars)):
            if stars[i][1] > y:
                stars[i] = (stars[i][0], stars[i][1] + expansion)
    for x in sorted(
        list(set(range(len(data[0]))).difference(x for x, _ in stars)), reverse=True
    ):
        for i in range(len(stars)):
            if stars[i][0] > x:
                stars[i] = (stars[i][0] + expansion, stars[i][1])

    dist = 0
    for c in combinations(stars, 2):
        dist += abs(c[0][0] - c[1][0]) + abs(c[0][1] - c[1][1])
    return dist


def prob_1(data: list[str]):
    return expand_and_calc_dist(data, 1)


def prob_2(data: list[str]):
    return expand_and_calc_dist(data, 999999)


def main():
    with open(INPUT or "input.txt", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    start = time.perf_counter()
    result = prob_1(data) if PART == 1 else prob_2(data)
    elapsed = time.perf_counter() - start

    print(f"Problem {PART}: {result}")
    print(f"Time: {elapsed} s")


if __name__ == "__main__":
    main()
