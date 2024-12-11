"""https://adventofcode.com/2024/day/10"""

import argparse
import time
from dataclasses import dataclass

# Input file path (default is "input.txt")
INPUT = "input.ex.txt"

# Part to solve, 1 or 2
PART = 1


def parse(data: list[str]):
    grid = {}
    heads = []
    for y in range(len(data)):
        for x in range(len(data[0])):
            grid[(x, y)] = -1 if data[y][x] == "." else int(data[y][x])
            if grid[(x, y)] == 0:
                heads.append((x, y))
    return grid, heads


@dataclass
class Node:
    pos: tuple[int, int]
    prev: "Node|None"


def score(h, grid):
    nines = set()
    q = [h]

    while q:
        p0 = q.pop(0)
        if grid[p0] == 9:
            nines.add(p0)
            continue

        for n in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            p1 = (p0[0] + n[0], p0[1] + n[1])
            if p1 in grid and grid[p1] == grid[p0] + 1:
                q.append(p1)
    return len(nines)


def rating(h, grid):
    paths = set()
    q = [Node(h, None)]

    while q:
        p0 = q.pop(0)
        if grid[p0.pos] == 9:
            n = p0
            path = []
            while n:
                path.insert(0, n.pos)
                n = n.prev
            paths.add(tuple(path))
            continue

        for n in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            p1 = (p0.pos[0] + n[0], p0.pos[1] + n[1])
            if p1 in grid and grid[p1] == grid[p0.pos] + 1:
                q.append(Node(p1, p0))
    return len(paths)


def prob_1(data: list[str]) -> int:
    grid, heads = parse(data)
    return sum(score(h, grid) for h in heads)


def prob_2(data: list[str]) -> int:
    grid, heads = parse(data)
    return sum(rating(h, grid) for h in heads)


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2024 day 10.")
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
