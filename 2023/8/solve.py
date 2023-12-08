#!/usr/bin/env python3

import math
import time

# https://adventofcode.com/2023/day/8

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


def main():
    with open(INPUT or "input.txt", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    start = time.perf_counter()
    result = prob_1(data) if PART == 1 else prob_2(data)
    elapsed = time.perf_counter() - start

    print(f"Problem {PART}: {result}")
    print(f"Time: {elapsed} s")


if __name__ == "__main__":
    main()
