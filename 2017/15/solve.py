"""https://adventofcode.com/2017/day/15"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1

A, B, MOD = 16807, 48271, 0x7FFFFFFF


def prob_1(data: list[str]) -> int:
    a, b = [int(line.split()[-1]) for line in data]
    total = 0
    for i in range(40_000_000):
        a = (a * A) % MOD
        b = (b * B) % MOD
        total += a & 0xFFFF == b & 0xFFFF
    return total


def prob_2(data: list[str]) -> int:
    a, b = [int(line.split()[-1]) for line in data]
    total = 0
    for i in range(5_000_000):
        while (a := (a * A) % MOD) & 0x3 != 0:
            pass
        while (b := (b * B) % MOD) & 0x7 != 0:
            pass
        total += a & 0xFFFF == b & 0xFFFF
    return total


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solves AoC 2017 day 15.")
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
