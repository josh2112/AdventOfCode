"""https://adventofcode.com/2024/day/20"""

import argparse
import heapq
import time
from collections import Counter

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def neighbors(p):
    for d in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        yield (p[0] + d[0], p[1] + d[1])


def parse(data: list[str]):
    endpts = [
        (x, y) for y, line in enumerate(data) for x, c in enumerate(line) if c in "SE"
    ]
    return (
        data,
        next(p for p in endpts if data[p[1]][p[0]] == "S"),
        next(p for p in endpts if data[p[1]][p[0]] == "E"),
    )


def prob_1(data: list[str], criteria: int) -> int:
    grid, start, end = parse(data)

    p, c = end, 0
    visited = {end: 0}  # loc: cost

    while True:
        if p == start:
            break
        c1 = c + 1
        for p1 in neighbors(p):
            if grid[p1[1]][p1[0]] != "#" and (p1 not in visited or c1 < visited[p1]):
                visited[p1] = c1
                p, c = p1, c1

    tally = Counter()

    for p in visited:
        for w in neighbors(p):
            if grid[w[1]][w[0]] == "#":
                for p2 in neighbors(w):
                    if p2 in visited and (sav := visited[p2] - visited[p] - 2) > 0:
                        tally[sav] += 1

    return sum(cnt for save, cnt in tally.items() if save >= criteria)


def prob_2(data: list[str]) -> int:
    print(data)
    return 0


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2024 day 20.")
    parser.add_argument("-p", "--part", choices=("1", "2", "all"), default=str(PART))
    parser.add_argument("-i", "--input", default=INPUT)
    args = parser.parse_args()
    part, infile = args.part, args.input

    with open(infile, mode="r", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    start = time.perf_counter()
    if part in ("1", "all"):
        print(f"Part 1: {prob_1(data, 100 if infile == 'input.txt' else 0)}")
    if part in ("2", "all"):
        print(f"Part 2: {prob_2(data, 100 if infile == 'input.txt' else 50)}")

    elapsed = time.perf_counter() - start
    print(f"Time: {elapsed} s")

    return elapsed


if __name__ == "__main__":
    main()
