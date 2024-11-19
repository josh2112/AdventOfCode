"""https://adventofcode.com/2015/day/3"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1

direc = {">": (1, 0), "^": (0, 1), "<": (-1, 0), "v": (0, -1)}


def prob_1(data: list[str]) -> int:
    counts = {(0, 0): 1}
    loc = (0, 0)
    for d in data[0]:
        delta = direc[d]
        loc = (loc[0] + delta[0], loc[1] + delta[1])
        v = counts.get(loc, 0)
        counts[loc] = v + 1
    return len(counts.keys())


def prob_2(data: list[str]) -> int:
    counts = {(0, 0): 2}
    santa, robot = (0, 0), (0, 0)
    is_robot = False
    for d in data[0]:
        delta = direc[d]
        if is_robot:
            robot = (robot[0] + delta[0], robot[1] + delta[1])
            v = counts.get(robot, 0)
            counts[robot] = v + 1
        else:
            santa = (santa[0] + delta[0], santa[1] + delta[1])
            v = counts.get(santa, 0)
            counts[santa] = v + 1
        is_robot = not is_robot

    return len(counts.keys())
    return 0


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2015 day 3.")
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
