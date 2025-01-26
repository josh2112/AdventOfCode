"""https://adventofcode.com/2017/day/12"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.ex.txt"

# Part to solve, 1 or 2
PART = 2


def parse(data: list[str]) -> dict[int, tuple[int, ...]]:
    return {
        src: set(map(int, line.split(" <-> ")[1].split(", ")))
        for src, line in enumerate(data)
    }


def fill_group(n, edges: dict[int, tuple[int, ...]], group: set[int] = set()):
    new = edges[n] - group
    group |= edges[n]
    for n in new:
        fill_group(n, edges, group)
    return group


def prob_1(data: list[str]) -> int:
    return len(fill_group(0, parse(data)))


def prob_2(data: list[str]) -> int:
    edges = parse(data)
    total = 0
    not_found = set(edges.keys())

    while not_found:
        not_found -= fill_group(next(n for n in not_found), edges)
        total += 1

    return total


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solves AoC 2017 day 12.")
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
