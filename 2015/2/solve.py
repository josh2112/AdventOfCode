"""https://adventofcode.com/2015/day/2"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def calc_paper(l: int, w: int, h: int):
    areas = (l * w, w * h, h * l)
    return 2 * sum(areas) + min(areas)


def calc_ribbon(l: int, w: int, h: int):
    sides = [l, w, h]
    sides.remove(max(sides))
    return l * w * h + 2 * sum(sides)


def prob_1(data: list[str]) -> int:
    return sum(calc_paper(*map(int, ln.split("x"))) for ln in data)


def prob_2(data: list[str]) -> int:
    return sum(calc_ribbon(*map(int, ln.split("x"))) for ln in data)
    return 0


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2015 day 2.")
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
