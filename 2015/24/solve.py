"""https://adventofcode.com/2015/day/24"""

import argparse
import itertools
import math
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def can_divide(pkgs: set[int], num_groups: int) -> bool:
    """Returns True if the packages can be divided evenly (by sum of weights) into num_groups groups"""
    for g2s in range(1, (len(pkgs) >> 1) + 1):
        if next(
            (
                g
                for g in itertools.combinations(pkgs, g2s)
                if sum(g) * (num_groups - 1) == sum(pkgs.difference(g))
            ),
            None,
        ):
            return True


def divide(data: list[str], num_groups: int) -> int:
    pkgs = set(sorted((int(ln) for ln in data), key=lambda x: -int(x)))
    num_groups -= 1

    # For each group 1 size 'g1s':
    for g1s in range(1, len(pkgs) - 1):
        # Find all the combos of g1s packages whose sum is 1/(num_groups-1) the sum of the remaining packages,
        # and whose remaining packages can be divided evenly into (num_groups-1) groups
        group1_configs = [
            g
            for g in itertools.combinations(pkgs, g1s)
            if sum(g) * num_groups == sum(pkgs.difference(g))
            and can_divide(pkgs.difference(g), num_groups)
        ]

        # If there are any, return the lowest min product of weights
        if group1_configs:
            return min(math.prod(g) for g in group1_configs)


def prob_1(data: list[str]) -> int:
    return divide(data, 3)


def prob_2(data: list[str]) -> int:
    return divide(data, 4)


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2015 day 24.")
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
