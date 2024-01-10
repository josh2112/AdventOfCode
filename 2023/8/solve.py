"""https://adventofcode.com/2023/day/8"""

import argparse
import math
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 2


def prob_1(data: list[str]):
    dirs = [1 if d == "R" else 0 for d in data[0]]
    nodes = {line[0:3]: (line[7:10], line[12:15]) for line in data[2:]}
    cur = "AAA"
    i = 0
    while cur != "ZZZ":
        cur = nodes[cur][dirs[i % len(dirs)]]
        i += 1
    return i


def prob_2(data: list[str]):
    dirs = [1 if d == "R" else 0 for d in data[0]]
    nodes = {line[0:3]: (line[7:10], line[12:15]) for line in data[2:]}
    curs = [n for n in nodes.keys() if n.endswith("A")]
    cycle_lengths = {}
    for cur in curs:
        n, i = cur, 0
        while n[2] != "Z":
            n = nodes[n][dirs[i % len(dirs)]]
            i += 1
        cycle_lengths[cur] = i
    return math.lcm(*cycle_lengths.values())


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2023 day 8.")
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
