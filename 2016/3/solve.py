"""https://adventofcode.com/2016/day/3"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def prob_1(data: list[str]) -> int:
    count = 0
    for line in data:
        sides = sorted(int(s) for s in line.split())
        count += 1 if sides[0] + sides[1] > sides[2] else 0
    return count


def prob_2(data: list[str]) -> int:
    count = 0
    tris = [[int(s) for s in line.split()] for line in data]
    for c in range(len(tris[0])):
        for r in range(0, len(tris), 3):
            sides = sorted((tris[r][c], tris[r + 1][c], tris[r + 2][c]))
            count += 1 if sides[0] + sides[1] > sides[2] else 0
    return count


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2016 day 3.")
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
