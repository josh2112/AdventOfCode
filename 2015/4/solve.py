"""https://adventofcode.com/2015/day/4"""

import argparse
import time
from hashlib import md5

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def find_hash_leading_zeros(data: str, num_zeroes: int):
    i = 1
    zeros = "0" * num_zeroes
    while True:
        if md5((f"{data}{i}").encode()).hexdigest().startswith(zeros):
            return i
        else:
            i += 1


def prob_1(data: list[str]) -> int:
    return find_hash_leading_zeros(data[0], 5)


def prob_2(data: list[str]) -> int:
    return find_hash_leading_zeros(data[0], 6)


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2015 day 4.")
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
