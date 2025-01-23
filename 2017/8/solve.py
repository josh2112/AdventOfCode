"""https://adventofcode.com/2017/day/8"""

import argparse
import time
import re
from collections import defaultdict

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def parse(data: str):
    for m in re.findall(r"(\w+) (inc|dec) (\-?\d+) if (\w+) ([!<=>]+) (\-?\d+)", data):
        yield m[0], int(m[2]) * (-1 if m[1] == "dec" else 1), m[3], m[4], int(m[5])


def run(data: str, part2: bool = False) -> int:
    reg = defaultdict(lambda: 0)
    maxval = 0
    for r1, inc, r2, cmp, val in list(parse(data)):
        match cmp:
            case "<":
                doit = reg[r2] < val
            case "<=":
                doit = reg[r2] <= val
            case ">":
                doit = reg[r2] > val
            case ">=":
                doit = reg[r2] >= val
            case "==":
                doit = reg[r2] == val
            case "!=":
                doit = reg[r2] != val
        if doit:
            reg[r1] += inc
            if inc > 0 and reg[r1] > maxval:
                maxval = reg[r1]

    return maxval if part2 else max(reg.values())


def prob_1(data: str) -> int:
    return run(data)


def prob_2(data: list[str]) -> int:
    return run(data, part2=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solves AoC 2017 day 8.")
    parser.add_argument("-p", "--part", choices=("1", "2", "all"), default=str(PART))
    parser.add_argument("-i", "--input", default=INPUT)
    args = parser.parse_args()

    with open(args.input, mode="r", encoding="utf-8") as f:
        data = f.read()

    start = time.perf_counter()
    if args.part in ("1", "all"):
        print(f"Part 1: {prob_1(data)}")
    if args.part in ("2", "all"):
        print(f"Part 2: {prob_2(data)}")

    print(f"Time: {time.perf_counter() - start} s")
