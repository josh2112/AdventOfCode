"""https://adventofcode.com/2016/day/15"""

import argparse
import re
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def prob_1(data: list[str]) -> int:
    discs = [
        (int(a), int(b))
        for a, b in re.findall(
            r"Disc #\d+ has (\d+) positions; at time=0, it is at position (\d+)\.",
            "\n".join(data),
        )
    ]

    t = 0
    while any(((t + i + 1 + d[1]) % d[0]) != 0 for i, d in enumerate(discs)):
        t += 1

    return t


def prob_2(data: list[str]) -> int:
    return prob_1(data + ["Disc #0 has 11 positions; at time=0, it is at position 0."])


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2016 day 15.")
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
