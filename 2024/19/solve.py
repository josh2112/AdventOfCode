"""https://adventofcode.com/2024/day/19"""

import argparse
import time
from functools import cache

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 2


@cache
def count_possibilities(towels: tuple[str, ...], pattern: str) -> int:
    return (
        1
        if not pattern
        else sum(
            count_possibilities(towels, pattern[len(t) :])
            for t in towels
            if pattern.startswith(t)
        )
    )


def prob_1(data: list[str]) -> int:
    towels, patterns = tuple(data[0].split(", ")), data[2:]
    return len([p for p in patterns if count_possibilities(towels, p)])


def prob_2(data: list[str]) -> int:
    towels, patterns = tuple(data[0].split(", ")), data[2:]
    return sum(count_possibilities(towels, p) for p in patterns)


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2024 day 19.")
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
