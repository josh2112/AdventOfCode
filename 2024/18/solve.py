"""https://adventofcode.com/2024/day/18"""

import argparse
import time
import heapq

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1

DIRS = ((1, 0), (0, 1), (-1, 0), (0, -1))


def prob_1(data: list[str]) -> int:
    walls = [tuple(int(v) for v in line.split(",")) for line in data]
    end = (max(w[0] for w in walls), max(w[1] for w in walls))

    walls = walls[:12]

    c0, p0 = 0, (0, 0)

    q = [(c0, p0)]  # cost, pos
    visited = {p0: c0}  # pos: cost

    while q:
        c0, p0 = heapq.heappop(q)
        if p0 == end:
            return c0

        c1 = c0 + 1
        for p1 in [(p0[0] + d[0], p0[1] + d[1]) for d in DIRS]:
            if p1 not in walls and (p1 not in visited or c1 < visited[p1]):
                visited[p1] = c1
                heapq.heappush(q, (c1, p1))


def prob_2(data: list[str]) -> int:
    print(data)
    return 0


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2024 day 18.")
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
