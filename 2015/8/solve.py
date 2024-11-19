"""https://adventofcode.com/2015/day/8"""

import argparse
import re
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def prob_1(data: list[str]) -> int:
    return sum(len(ln) for ln in data) - sum(
        len(
            re.sub(
                r"\\x[0-9a-f][0-9a-f]",
                "X",
                line[1:-1].replace("\\\\", "\\").replace('\\"', '"'),
            )
        )
        for line in data
    )


def prob_2(data: list[str]) -> int:
    return sum(
        len(line.replace("\\", "\\\\").replace('"', '\\"')) + 2 for line in data
    ) - sum(len(ln) for ln in data)


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2015 day 8.")
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
