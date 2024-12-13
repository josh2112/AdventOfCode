"""https://adventofcode.com/2024/day/11"""

import argparse
import time
from collections import Counter

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def solve(data: list[str], blinks: int) -> int:
    stonecounts = Counter(data[0].split())

    for n in range(blinks):
        newcounts = Counter()
        for s in stonecounts:
            # 0 becomes 1
            if s == "0":
                newcounts["1"] += stonecounts[s]
            # even numbers are split in half
            elif not (len(s) % 2):
                half = len(s) // 2
                newcounts[str(int(s[:half]))] += stonecounts[s]
                newcounts[str(int(s[half:]))] += stonecounts[s]
            # all others are multiplied by 2024
            else:
                newcounts[str(int(s) * 2024)] += stonecounts[s]
        stonecounts = newcounts

    return len(stonecounts)


def prob_1(data: list[str]) -> int:
    return solve(data, 25)


def prob_2(data: list[str]) -> int:
    return solve(data, 75)


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2024 day 11.")
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
