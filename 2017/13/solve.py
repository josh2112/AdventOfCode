"""https://adventofcode.com/2017/day/13"""

import argparse
import time
from itertools import count

# Input file path (default is "input.txt")
INPUT = "input.ex.txt"

# Part to solve, 1 or 2
PART = 2


def parse(data: list[str]):
    for line in data:
        d, r = [int(x) for x in line.split(": ")]
        yield d, r, (r - 1) * 2


def prob_1(data: list[str]) -> int:
    return sum(d * r for d, r, p in parse(data) if not d % p)


def prob_2(data: list[str]) -> int:
    layers = list(parse(data))
    return next(i for i in count() if all((d + i) % p for d, _, p in layers))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solves AoC 2017 day 13.")
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
