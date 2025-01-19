"""https://adventofcode.com/2017/day/2"""

import argparse
import time
import itertools
import math

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def prob_1(data: list[str]) -> int:
    return sum(
        max(nums) - min(nums)
        for nums in [list(map(int, line.split())) for line in data]
    )


def prob_2(data: list[str]) -> int:
    return sum(
        max(pair) // min(pair)
        for nums in [list(map(int, line.split())) for line in data]
        for pair in itertools.combinations(nums, 2)
        if math.gcd(*pair) in pair
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solves AoC 2017 day 2.")
    parser.add_argument("-p", "--part", choices=("1", "2", "all"), default=str(PART))
    parser.add_argument("-i", "--input", default=INPUT)
    args = parser.parse_args()

    with open(args.input, mode="r", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    start = time.perf_counter()
    if args.part in ("1", "all"):
        print(f"Part 1: {prob_1(data)}")
    if args.part in ("2", "all"):
        print(f"Part 2: {prob_2(data)}")

    print(f"Time: {time.perf_counter() - start} s")
