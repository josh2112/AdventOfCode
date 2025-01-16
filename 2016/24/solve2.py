"""https://adventofcode.com/2016/day/24"""

import argparse
import heapq
import itertools
import time
from collections import defaultdict

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def parse(data: list[str]):
    spaces, goals, start = [], [], None
    for y, line in enumerate(data[1:-1]):
        for x, c in enumerate(line[1:-1]):
            if c == "." or str.isnumeric(c):
                spaces.append((x, y))
                if str.isnumeric(c):
                    goals.append((x, y))
                    if c == "0":
                        start = (x, y)

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

    edges = defaultdict(set[tuple[int, int]])

    q = [(0, start)]
    v = {start: 0}

    while q:
        c0, p0 = heapq.heappop(q)

        for d in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            p1, c1 = walk(p0, d)
            if c1 > 0:
                if p1 not in v or c1 < v[p1]:
                    v[p1] = c1
                    edges[p0].add(p1)
                    edges[p1].add(p0)
                    heapq.heappush(q, (c1, p1))

    return edges, goals, start


def shortest_path(start, end, edges):
    q = [(0, start)]
    v = {start: 0}

    while q:
        c0, p0 = heapq.heappop(q)

        if p0 == end:
            return c0

        for p1 in edges[p0]:
            c1 = c0 + abs(p0[0] - p1[0]) + abs(p0[1] - p1[1])
            if p1 not in v or c1 < v[p1]:
                v[p1] = c1
                heapq.heappush(q, (c1, p1))


# TODO: This returns 496 (wrong) in 1.3 seconds, while solve.py returns 456 (correct) in 73 seconds. What's wrong here??
def prob_1(data: list[str]) -> int:
    edges, goals, p0 = parse(data)

    dist = dict()

    for start, end in itertools.combinations(goals, r=2):
        dist[(start, end)] = dist[(end, start)] = shortest_path(start, end, edges)

    goals = set(goals)

    q = [(0, frozenset([p0]), p0)]  # steps taken, goals hit, position
    v = {(p0, frozenset([p0])): 0}

    while q:
        c0, gh0, p0 = heapq.heappop(q)

        if goals.issubset(gh0):
            return c0

        for p1 in [pr[1] for pr in dist if pr[0] == p0]:
            c1 = c0 + dist[(p0, p1)]
            gh1 = frozenset(gh0 | set([p1]))
            if (p1, gh1) not in v or c1 < v[(p1, gh1)]:
                v[(p1, gh1)] = c1
                heapq.heappush(q, (c1, gh1, p1))


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
