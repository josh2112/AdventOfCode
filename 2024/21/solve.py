"""https://adventofcode.com/2024/day/21"""

import argparse
import time
import heapq
from functools import cache

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def neighbors(p):
    for d in ((-1, 0, "<"), (1, 0, ">"), (0, -1, "^"), (0, 1, "v")):
        yield (p[0] + d[0], p[1] + d[1]), d[2]


@cache
def shortest_path(grid, start, end) -> list[tuple[int, int]]:
    q = [(0, start, [])]  # cost, cur, path
    visited = {start: 0}  # loc: cost
    w, h = len(grid[0]), len(grid)

    while q:
        c, p, path = heapq.heappop(q)
        if p == end:
            return path
        c1 = c + 1
        for p1, d1 in neighbors(p):
            if (
                not (0 <= p1[0] < w)
                or not (0 <= p1[1] < h)
                or grid[p1[1]][p1[0]] == " "
            ):
                continue
            if p1 not in visited or c1 < visited[p1]:
                visited[p1] = c1
                heapq.heappush(q, (c1, p1, path + [d1]))


def prob_1(data: list[str]) -> int:
    kp_door = ("789", "456", "123", " 0A")
    kp_bot = (" ^A", "<v>")

    keys_door = {c: (x, y) for y, row in enumerate(kp_door) for x, c in enumerate(row)}
    keys_bot = {c: (x, y) for y, row in enumerate(kp_bot) for x, c in enumerate(row)}

    d = (2, 3)
    d_path = []
    for code in data[:1]:
        for key in code:
            d1 = keys_door[key]
            d_path += shortest_path(kp_door, d, d1) + ["A"]
            d = d1

    b0 = (2, 0)
    b0_path = []
    for key in d_path:
        nxt = keys_bot[key]
        b0_path += shortest_path(kp_bot, b0, nxt) + ["A"]
        b0 = nxt

    b1 = (2, 0)
    b1_path = []
    for key in b0_path:
        nxt = keys_bot[key]
        b1_path += shortest_path(kp_bot, b1, nxt) + ["A"]
        b1 = nxt

    return "".join(b1_path), len(b1_path)


def prob_2(data: list[str]) -> int:
    print(data)
    return 0


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
