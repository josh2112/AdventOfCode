"""https://adventofcode.com/2015/day/17"""

import argparse
import time
from itertools import chain, combinations

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def prob_1(data: list[str]) -> int:
    containers = [int(line) for line in data]
    amount = 25 if containers[0] == 20 else 150
    return len(
        [
            c
            for lst in (
                (combinations(containers, n)) for n in range(1, len(containers) + 1)
            )
            for c in lst
            if sum(c) == amount
        ]
    )


def prob_2(data: list[str]) -> int:
    containers = [int(line) for line in data]
    amount = 25 if containers[0] == 20 else 150
    combos = [
        c
        for lst in (
            (combinations(containers, n)) for n in range(1, len(containers) + 1)
        )
        for c in lst
        if sum(c) == amount
    ]
    min_container_count = min(len(c) for c in combos)
    return sum(1 if len(c) == min_container_count else 0 for c in combos)


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2015 day 17.")
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
