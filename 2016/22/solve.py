"""https://adventofcode.com/2016/day/22"""

import argparse
import heapq
import re
import time
from dataclasses import dataclass
from itertools import combinations

# Input file path (default is "input.txt")
INPUT = "input.ex.txt"

# Part to solve, 1 or 2
PART = 2


@dataclass
class Node:
    x: int
    y: int
    size: int
    used: int


def parse(data: list[str]):
    for line in re.findall(r"x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T", "\n".join(data[2:])):
        yield Node(*[int(v) for v in line])


def prob_1(data: list[str]) -> int:
    nodes = list(parse(data))
    return sum(
        1 if pr[a].used > 0 and pr[b].size - pr[b].used >= pr[a].used else 0
        for pr in combinations(nodes, r=2)
        for a, b in ((0, 1), (1, 0))
    )


def reconstruct_path(states, nodes):
    # (for debugging) prints the node grid (used/total) and moves state-by-state
    w, h = max(n.x for n in nodes.values()) + 1, max(n.y for n in nodes.values()) + 1
    f0 = None
    for g, f, used in states:
        if f0:
            print(f"\n---[{f0} -> {f}]---")
        for y in range(h):
            line = ""
            for x in range(w):
                p = (x, y)
                tmp = f"{used[p] if p in used else nodes[p].used}/{nodes[p].size}"
                if p == g:
                    tmp = f"({tmp})"
                tmp = f"{tmp: >8}"
                line += tmp
            print(line)
        f0 = f


def prob_2(data: list[str]) -> int:
    nodes = {(n.x, n.y): n for n in list(parse(data))}

    # Get node's used space (from original node, or used array if updated)
    def used(p, u):
        return u[p] if p in u else nodes[p].used

    goal = (max(n.x for n in nodes.values()), 0)
    free = next((n.x, n.y) for n in nodes.values() if n.used == 0)

    # Cost, goal, free, (x,y) => updated used value, state list
    q = [(0, goal, free, dict(), [])]

    # Best cost to get goal and free to these positions
    visited = {(goal, free): 0}

    while q:
        c0, g0, f0, used0, s0 = heapq.heappop(q)

        if g0 == (0, 0):
            # reconstruct_path(s0 + [(g0, f0, used0)], nodes)
            return c0

        # Move the free space around (U,R,D,L)
        for d in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            f1 = (f0[0] + d[0], f0[1] + d[1])

            # Is f1 a valid node, and is f0 big enough to hold the data in f1?
            if f1 not in nodes or nodes[f0].size < used(f1, used0):
                continue

            # Are we moving the goal?
            c1, g1 = c0 + 1, f0 if f1 == g0 else g0

            if (g1, f1) not in visited or c1 < visited[(g1, f1)]:
                visited[(g1, f1)] = c1
                # update our 'used' array with the 2 new changed nodes
                used1 = used0.copy()
                used1[f1], used1[f0] = 0, used(f1, used0)
                heapq.heappush(q, (c1, g1, f1, used1, s0 + [(g0, f0, used0)]))


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2016 day 22.")
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
