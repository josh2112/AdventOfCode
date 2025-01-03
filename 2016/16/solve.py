"""https://adventofcode.com/2016/day/16"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def dragon(a):
    return a + [0] + [0 if c else 1 for c in reversed(a)]


def checksum(a, ln):
    for i in range(0, ln, 2):
        a[i >> 1] = 1 if a[i] == a[i + 1] else 0
    return ln >> 1


def calc(a, ln):
    while len(a) < ln:
        a = dragon(a)

    a = a[:ln]
    while True:
        ln = checksum(a, ln)
        if ln % 2:
            break

    return "".join(str(i) for i in a[:ln])


def prob_1(data: list[str]) -> int:
    # return calc( [1, 0, 0, 0, 0], 20 ) # Example
    return calc([int(i) for i in data[0]], 272)


def prob_2(data: list[str]) -> int:
    return calc([int(i) for i in data[0]], 35651584)


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2016 day 16.")
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
