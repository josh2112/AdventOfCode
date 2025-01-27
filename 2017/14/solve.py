"""https://adventofcode.com/2017/day/14"""

import argparse
import os
import sys
import time
from importlib import import_module

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
general_knot_hash = getattr(import_module("10.solve"), "general_knot_hash")


# Input file path (default is "input.txt")
INPUT = "input.ex.txt"

# Part to solve, 1 or 2
PART = 2


def prob_1(data: list[str]) -> int:
    return sum(
        sum(
            h.bit_count() for h in general_knot_hash([ord(c) for c in f"{data[0]}-{i}"])
        )
        for i in range(128)
    )


def fill_group(cells: set[tuple[int, int]], seed: tuple[int, int]):
    if seed in cells:
        cells.remove(seed)
        for d in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            fill_group(cells, (seed[0] + d[0], seed[1] + d[1]))


def prob_2(data: list[str]) -> int:
    cells = set()
    for y in range(128):
        for x, h in enumerate(general_knot_hash([ord(c) for c in f"{data[0]}-{y}"])):
            for i, c in enumerate(f"{h:08b}"):
                if c == "1":
                    cells.add((x * 8 + i, y))

    groups = 0
    while cells:
        fill_group(cells, next(c for c in cells))
        groups += 1

    return groups


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solves AoC 2017 day 14.")
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
