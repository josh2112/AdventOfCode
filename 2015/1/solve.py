"""https://adventofcode.com/2015/day/1"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def prob_1(data: list[str]) -> int:
    floor = 0
    for c in data[0]:
        if c == "(":
            floor += 1
        else:
            floor -= 1
    return floor


def prob_2(data: list[str]) -> int:
    floor = 0
    for i, c in enumerate(data[0]):
        if c == "(":
            floor += 1
        else:
            floor -= 1
        if floor == -1:
            return i + 1
    return 0


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2015 day 1.")
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
