#!/usr/bin/env python3

import time

# https://adventofcode.com/$year/day/$day

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def prob_1(data: list[str]):
    print(data)


def prob_2(data: list[str]):
    print(data)


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
