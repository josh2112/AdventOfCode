"""https://adventofcode.com/2016/day/24"""

import argparse
import time
import heapq

# Input file path (default is "input.txt")
INPUT = "input.ex.txt"

# Part to solve, 1 or 2
PART = 1


def parse(data: list[str]):
    spaces, goals, start = [], set(), None
    for y, line in enumerate(data[1:-1]):
        for x, c in enumerate(line[1:-1]):
            if c == "." or str.isnumeric(c):
                spaces.append((x, y))
                if str.isnumeric(c):
                    goals.add((x, y))
                    if c == "0":
                        start = (x, y)
    return spaces, goals, start


def prob_1(data: list[str]) -> int:
    spaces, goals, p0 = parse(data)
    goals.remove(p0)

    # steps taken, num goals remaining, outstanding goals, position
    q = [(0, len(goals), goals, p0)]

    # (position, num goals remaining) -> steps taken
    v = {(p0, len(goals)): 0}

    while q:
        c0, n0, g0, p0 = heapq.heappop(q)

        if n0 == 0:
            return c0

        c1 = c0 + 1

        for d in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            if (p1 := (p0[0] + d[0], p0[1] + d[1])) in spaces:
                g1, n1 = g0 - set((p1,)), n0
                if len(g1) < len(g0):
                    n1 -= 1
                if (p1, n1) not in v or c1 < v[(p1, n1)]:
                    v[(p1, n1)] = c1
                    heapq.heappush(q, (c1, n1, g1, p1))


def prob_2(data: list[str]) -> int:
    print(data)
    return 0


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2016 day 24.")
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
