"""https://adventofcode.com/2022/day/24"""

import argparse
import heapq
import time

# Input file path (default is "input.txt")
INPUT = "input.ex2.txt"

# Part to solve, 1 or 2
PART = 2

DIRS = {"<": (-1, 0), "^": (0, -1), ">": (1, 0), "v": (0, 1)}


def parse(data: list[str]):
    bounds = (len(data[0]) - 2, len(data) - 2)
    start, goal = (0, -1), (len(data[-1]) - 3, len(data) - 2)
    blizzards = [
        ((x - 1, y - 1), c)
        for y, row in enumerate(data)
        for x, c in enumerate(row)
        if c in DIRS.keys()
    ]
    return bounds, start, goal, blizzards


def fast_forward(blizzards, bounds, t: int):
    """Returns the blizzard positions and directions at time t"""
    projected = []
    for bliz in blizzards:
        (x, y), (dx, dy) = bliz[0], DIRS[bliz[1]]
        projected.append(
            (((x + dx * t) % bounds[0], (y + dy * t) % bounds[1]), bliz[1])
        )
    return projected


def project_empty(blizzards, bounds, t: int) -> list[tuple[int, int]]:
    """Returns a list of coords that will be empty at time t"""
    projected = [[False for x in range(bounds[0])] for y in range(bounds[1])]

    for bliz in fast_forward(blizzards, bounds, t):
        projected[bliz[0][1]][bliz[0][0]] = True

    return set(
        [
            (x, y)
            for y in range(bounds[1])
            for x in range(bounds[0])
            if not projected[y][x]
        ]
    )


def shortest_path(bounds, start, goal, blizzards):
    def neighbors(p):
        yield from ((p[0] + d[0], p[1] + d[1]) for d in DIRS.values())

    empty_at_t = [project_empty(blizzards, bounds, 0)]

    q = [(0, start)]  # time, taxicab dist from goal, pos

    visited_at_t = [set([start])]

    while q:
        t0, p0 = heapq.heappop(q)

        if p0 == goal:
            return t0

        t1 = t0 + 1
        if t1 == len(empty_at_t):
            empty_at_t.append(project_empty(blizzards, bounds, t1))

        if t1 == len(visited_at_t):
            visited_at_t.append(set())

        for p1 in neighbors(p0):
            if p1 == goal or (p1 in empty_at_t[t1] and p1 not in visited_at_t[t1]):
                heapq.heappush(q, (t1, p1))
                visited_at_t[t1].add(p1)

        # Also add the case where we don't move
        if p0 == start or p0 in empty_at_t[t1] and p0 not in visited_at_t[t1]:
            heapq.heappush(q, (t1, p0))
            visited_at_t[t1].add(p0)

    return 0


def traverse(bounds, start, goal, blizzards, rounds: int = 1):
    for i in range(rounds):
        # Traverse once, yield the time, and set up for the next traversal
        yield (t := shortest_path(bounds, start, goal, blizzards))
        blizzards = fast_forward(blizzards, bounds, t)
        start, goal = goal, start


def prob_1(data: list[str]) -> int:
    return sum(traverse(*parse(data)))


def prob_2(data: list[str]) -> int:
    return sum(traverse(*parse(data), 3))


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2022 day 24.")
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
