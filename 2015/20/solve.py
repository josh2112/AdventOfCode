"""https://adventofcode.com/2015/day/20"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 2


def distribute_presents(limit: int, multiple: int, target: int, elf_limit=None):
    houses = [multiple] * (limit + 1)
    for i in range(2, limit + 1):
        for j in range(i, limit + 1, i)[:elf_limit]:
            houses[j] += i * multiple
    return next((i for i, h in enumerate(houses) if h >= target), None)


def prob_1(data: list[str]) -> int:
    return distribute_presents(1_000_000, 10, int(data[0]))


def prob_2(data: list[str]) -> int:
    return distribute_presents(1_000_000, 11, int(data[0]), 50)
    return 0


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2015 day 20.")
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
