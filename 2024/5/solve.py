"""https://adventofcode.com/2024/day/5"""

import argparse
import time
from itertools import combinations

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def parse(data: list[str]):
    split = data.index("")
    return [tuple(map(int, pr.split("|"))) for pr in data[:split]], [
        tuple(map(int, u.split(","))) for u in data[split + 1 :]
    ]


def prob_1(data: list[str]) -> int:
    rules, updates = parse(data)
    accum = 0
    for u in updates:
        reversed_combos = list(combinations(reversed(u), 2))
        if not any(r in reversed_combos for r in rules):
            accum += u[len(u) // 2]

    return accum


def prob_2(data: list[str]) -> int:
    rules, updates = parse(data)
    accum = 0
    for u in updates:
        if any(r in list(combinations(reversed(u), 2)) for r in rules):
            while True:
                mistakes = [r for r in rules if r in list(combinations(reversed(u), 2))]
                if not mistakes:
                    break
                u = list(u)
                for m in mistakes:
                    i1, i2 = u.index(m[0]), u.index(m[1])
                    if i1 > i2:
                        n2 = u.pop(i2)
                        u.insert(i1, n2)
            accum += u[len(u) // 2]

    return accum


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2024 day 5.")
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
