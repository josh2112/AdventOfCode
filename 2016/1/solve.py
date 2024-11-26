"""https://adventofcode.com/2016/day/1"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1

DIRS = ((0, 1), (1, 0), (0, -1), (-1, 0))


def prob_1(data: list[str]) -> int:
    x, y, diridx = 0, 0, 0
    for inst in data[0].split(", "):
        dist = int(inst[1:])
        diridx = ((1 if inst[0] == "R" else -1) + diridx) % len(DIRS)
        x += DIRS[diridx][0] * dist
        y += DIRS[diridx][1] * dist

    return abs(x) + abs(y)


def prob_2(data: list[str]) -> int:
    diridx = 0
    visited = [(0, 0)]
    for inst in data[0].split(", "):
        dist = int(inst[1:])
        diridx = ((1 if inst[0] == "R" else -1) + diridx) % len(DIRS)
        c = visited[-1]
        for i in range(1, dist + 1):
            v = (c[0] + DIRS[diridx][0] * i, c[1] + DIRS[diridx][1] * i)
            if v in visited:
                return abs(v[0]) + abs(v[1])
            else:
                visited.append(v)

    return abs(visited[-1][0]) + abs(visited[-1][1])


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2016 day 1.")
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
