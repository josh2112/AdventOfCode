"""https://adventofcode.com/2016/day/2"""

import argparse
import time
from itertools import product

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1

DIRS = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0)}


def prob_1(data: list[str]) -> int:
    code, b = [], (1, 1)
    for line in data:
        for d in line:
            b = (
                min(max(DIRS[d][0] + b[0], 0), 2),
                min(max(DIRS[d][1] + b[1], 0), 2),
            )
            # print(f"{d} {b} '{b[1] * 3 + b[0] + 1}'")
        code.append(b[1] * 3 + b[0] + 1)

    return "".join(str(c) for c in code)


def prob_2(data: list[str]) -> int:
    kp = ("  1  ", " 234 ", "56789", " ABC ", "  D  ")
    size = len(kp[0])
    keypad = {c: kp[c[1]][c[0]] for c in product(range(size), repeat=2)}

    code, b = [], (0, 2)
    for line in data:
        for d in line:
            bnew = (
                min(max(DIRS[d][0] + b[0], 0), size - 1),
                min(max(DIRS[d][1] + b[1], 0), size - 1),
            )
            if keypad[bnew] != " ":
                b = bnew
                # print(f"{d} {b} '{keypad[b]}'")
        # print("next digit:", keypad[b])
        code.append(keypad[b])

    return "".join(str(c) for c in code)


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2016 day 2.")
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
