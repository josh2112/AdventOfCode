"""https://adventofcode.com/2024/day/16"""

import argparse
import time
from dataclasses import dataclass
from heapq import heappop, heappush
from sys import maxsize

# Input file path (default is "input.txt")
INPUT = "input.ex.txt"

# Part to solve, 1 or 2
PART = 1


DIRS = ((1, 0), (0, 1), (-1, 0), (0, -1))
ARROWS = {(1, 0): "→", (0, 1): "↓", (-1, 0): "←", (0, -1): "↑"}


def parse(data: list[str]):
    walls = set()
    start, end = None, None
    for y, line in enumerate(data[1:-1]):
        for x, c in enumerate(line[1:-1]):
            if c == "#":
                walls.add((x, y))
            elif c == "S":
                start = (x, y)
            elif c == "E":
                end = (x, y)
    return (len(data[0]) - 2, len(data) - 2), walls, start, end


@dataclass(frozen=True, order=True)
class Node:
    pos: tuple[int, int]
    direction: tuple[int, int]
    prev: "Node|None" = None


def prob_1(data: list[str]) -> int:
    size, walls, start, end = parse(data)

    root = Node(start, (1, 0))

    q = [(0, root)]

    visited = {(root.pos, root.direction): 0}

    while q:
        c0, n0 = heappop(q)
        p0, d0 = n0.pos, n0.direction

        if p0 == end:
            return c0

        # print(f"{p0} => {d0} ({c0})")
        # Options: each of the 4 directions and straight ahead
        for d1 in (
            DIRS[(DIRS.index(d0) - 1) % len(DIRS)],
            DIRS[(DIRS.index(d0) + 1) % len(DIRS)],
        ):
            p1 = (p0[0] + d1[0], p0[1] + d1[1])
            # Make sure a direction is valid (not out-of-bounds or a wall) and different from current
            if (
                d1 != d0
                and p1 not in walls
                and 0 <= p1[0] < size[0]
                and 0 <= p1[1] < size[1]
            ):
                c1 = c0 + 1000
                if (p0, d1) not in visited or c1 < visited[(p0, d1)]:
                    # print(f" * can turn to {d1} for cost {c1}")
                    n1 = Node(p0, d1, n0)
                    heappush(q, (c1, n1))
                    visited[(p0, d1)] = c1
        p1 = (p0[0] + d0[0], p0[1] + d0[1])
        if p1 not in walls and 0 <= p1[0] < size[0] and 0 <= p1[1] < size[1]:
            c1 = c0 + 1
            if (p1, d0) not in visited or c1 < visited[(p1, d0)]:
                # print(f" * can move to {p1} for cost {c1}")
                n1 = Node(p1, d0, n0)
                heappush(q, (c1, n1))
                visited[(p1, d0)] = c1


def prob_2(data: list[str]) -> int:
    size, walls, start, end = parse(data)

    best_cost = prob_1(data)

    root = Node(start, (1, 0))

    q = [(0, root)]

    best_cost = maxsize
    tiles_on_best_paths = set()

    visited = {(root.pos, root.direction): 0}

    while q:
        c0, n0 = heappop(q)
        p0, d0 = n0.pos, n0.direction

        if p0 == end and c0 <= best_cost:
            best_cost = c0
            print(f"Found best path (c={c0})")
            while n0:
                tiles_on_best_paths.add(n0.pos)
                n0 = n0.prev
            continue

        # print(f"{p0} => {ARROWS[d0]} ({c0})")
        # Options: each of the 4 directions and straight ahead
        for d1 in (
            DIRS[(DIRS.index(d0) - 1) % len(DIRS)],
            DIRS[(DIRS.index(d0) + 1) % len(DIRS)],
        ):
            p1 = (p0[0] + d1[0], p0[1] + d1[1])
            # Make sure a direction is valid (not out-of-bounds or a wall) and different from current
            if (
                d1 != d0
                and p1 not in walls
                and 0 <= p1[0] < size[0]
                and 0 <= p1[1] < size[1]
            ):
                c1 = c0 + 1000
                # Import change from part 1: <= here, since there are multiple best paths
                if c1 < best_cost and (
                    (p0, d1) not in visited or c1 <= visited[(p0, d1)]
                ):
                    # print(f" * can turn {ARROWS[d1]} for total cost {c1}")
                    n1 = Node(p0, d1, n0)
                    heappush(q, (c1, n1))
                    visited[(p0, d1)] = c1
        p1 = (p0[0] + d0[0], p0[1] + d0[1])
        if p1 not in walls and 0 <= p1[0] < size[0] and 0 <= p1[1] < size[1]:
            c1 = c0 + 1
            # Import change from part 1: <= here, since there are multiple best paths
            if c1 < best_cost and ((p1, d0) not in visited or c1 <= visited[(p1, d0)]):
                # print(f" * can move to {p1} for total cost {c1}")
                n1 = Node(p1, d0, n0)
                heappush(q, (c1, n1))
                visited[(p1, d0)] = c1

    # printmaze(size, walls, tiles_on_best_paths)

    return len(tiles_on_best_paths)


def printmaze(size, walls, tiles_on_best_paths):
    grid = [[" "] * size[0] for i in range(size[1])]
    for w in walls:
        grid[w[1]][w[0]] = "░"
    for t in tiles_on_best_paths:
        grid[t[1]][t[0]] = "•"
    print("\n".join("".join(row) for row in grid))


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2024 day 16.")
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
