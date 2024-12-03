"""https://adventofcode.com/2024/day/3"""

import argparse
import time
import re

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def prob_1(data: list[str]) -> int:
    return sum(
        int(m[0]) * int(m[1]) for m in re.findall(r"mul\((\d+),(\d+)\)", "".join(data))
    )


def prob_2(data: list[str]) -> int:
    accum = 0
    on = True
    for m in re.findall(r"(mul\((\d+),(\d+)\))|(do\(\))|(don't\(\))", "".join(data)):
        if on and m[0]:
            accum += int(m[1]) * int(m[2])
        else:
            on = m[3] and not m[4]
    return accum


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2024 day 3.")
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
