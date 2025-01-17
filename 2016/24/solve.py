"""https://adventofcode.com/2016/day/24"""

import argparse
import heapq
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

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

    # From point p, walk in direction d until we hit a goal or wall or see an intersection (a space on either side).
    # Return last point and number of steps taken.
    def walk(p, d):
        perpdirs = ((0, 1), (0, -1)) if d[1] == 0 else ((1, 0), (-1, 0))
        c = 0
        while (p1 := (p[0] + d[0], p[1] + d[1])) in spaces:
            c += 1
            # Have we hit an intersection or a goal?
            if (
                any((p1[0] + d1[0], p1[1] + d1[1]) in spaces for d1 in perpdirs)
                or p1 in goals
            ):
                return p1, c
            p = p1
        return p, c

    # steps taken, num goals remaining, outstanding goals, position, path
    q = [(0, len(goals), goals, p0, [p0])]

    # (position, outstanding goals) -> steps taken
    v = {(p0, frozenset(goals)): 0}

    while q:
        c0, n0, g0, p0, path = heapq.heappop(q)

        # print(f"Step {c0}: exploring from {p0} with {n0} goal(s) left: {g0}")

        if n0 == 0:
            return c0, path

        for d in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            p1, dc = walk(p0, d)
            if dc > 0:
                c1 = c0 + dc
                g1 = frozenset(g0 - set((p1,)))
                n1 = n0 - len(g0) + len(g1)
                if (p1, g1) not in v or c1 < v[(p1, g1)]:
                    v[(p1, g1)] = c1
                    heapq.heappush(q, (c1, n1, g1, p1, path + [p1]))


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
