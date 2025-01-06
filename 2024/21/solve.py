"""https://adventofcode.com/2024/day/21"""

import argparse
import heapq
import time
from functools import cache

# Input file path (default is "input.txt")
INPUT = "input.ex.txt"

# Part to solve, 1 or 2
PART = 2

DIRS = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)}


def neighbors(p):
    for symbol, delta in DIRS.items():
        yield (p[0] + delta[0], p[1] + delta[1]), symbol


@cache
def best_paths(grid, start: tuple[int, int], end: tuple[int, int]):
    q = [(0, start, [])]  # cost, cur, path
    w, h = len(grid[0]), len(grid)

    best_cost = abs(end[1] - start[1]) + abs(end[0] - start[0])
    best_paths = []

    while q:
        c, p, path = heapq.heappop(q)
        if c >= best_cost and p != end:
            continue
        if p == end:
            best_paths.append(path + ["A"])
            continue
        for p1, d1 in neighbors(p):
            if (0 <= p1[0] < w) and (0 <= p1[1] < h) and grid[p1[1]][p1[0]] != " ":
                heapq.heappush(q, (c + 1, p1, path + [d1]))

    return best_paths


def dfs(codes, depth):
    grid_door = ("789", "456", "123", " 0A")
    grid_bot = (" ^A", "<v>")

    keymap_door, keymap_bot = tuple(
        {c: (x, y) for y, row in enumerate(kp) for x, c in enumerate(row)}
        for kp in (grid_door, grid_bot)
    )

    @cache
    def calc(path, depth):
        if depth == 0:
            return len(path)
        else:
            return sum(
                min(
                    calc(tuple(p), depth - 1)
                    for p in best_paths(grid_bot, *[keymap_bot[k] for k in pr])
                )
                for pr in zip(["A"] + list(path), path)
            )

    complexity = 0

    for code in codes:
        cost = 0
        for pr in zip(["A"] + [c for c in code], code):
            cost += min(
                calc(tuple(p), depth)
                for p in best_paths(grid_door, *[keymap_door[k] for k in pr])
            )
        # print(f"Code {code}: {cost}")
        complexity += cost * int(code[:-1])

    return complexity


def prob_1(data: list[str]) -> int:
    return dfs(data, 2)


def prob_2(data: list[str]) -> int:
    return dfs(data, 25)


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2024 day 21.")
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
