#!/usr/bin/env python3

import math
import time

# https://adventofcode.com/2023/day/18

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1

dirs = {"R": (1, 0), "U": (0, -1), "D": (0, 1), "L": (-1, 0)}
dirs_ordered = ["R", "D", "L", "U"]


def flood_fill(border: set[tuple[int, int]], x: int, y: int):
    stack: set[tuple[int, int]] = set([(x, y)])
    while stack:
        n = stack.pop()
        border.add(n)
        for n1 in (
            (n[0] - 1, n[1]),
            (n[0] + 1, n[1]),
            (n[0], n[1] - 1),
            (n[0], n[1] + 1),
        ):
            if n1 not in border:
                stack.add(n1)


def outline(instrs: list[tuple[int, str]]):
    loc = (0, 0)
    cubes: set[tuple[int, int]] = set([loc])
    i = 0
    coords = []
    for num, dr in instrs:
        vec = dirs[dr]
        for _ in range(int(num)):
            loc = (loc[0] + vec[0], loc[1] + vec[1])
            cubes.add(loc)
        coords.append(loc)
        i += 1
        # print(f"{i}/{len(instrs)}")

    with open(f"tmp-part{PART}.svg", "w") as f:
        f.write('<svg><path d="')
        f.write("M0 0 " + " ".join(f"L{c[0]} {c[1]}" for c in coords) + " Z")
        f.write('"/></svg>')

    for y in range(min(y for _, y in cubes), max(y for _, y in cubes) + 1):
        coords = [
            x for x, _ in sorted((c for c in cubes if c[1] == y), key=lambda c: c[0])
        ]
        if len(coords) > 1 and coords[1] - coords[0] > 1:
            # We found a good inside coordinate!
            flood_fill(cubes, coords[0] + 1, y)
            break
    return len(cubes)


def prob_1(data: list[str]):
    instrs = [(int(num), dr) for dr, num, _ in [line.split() for line in data]]
    loc = (0, 0)
    coords = [loc]
    for num, dr in instrs:
        loc = (loc[0] + dirs[dr][0] * num, loc[1] + dirs[dr][1] * num)
        coords.append(loc)
    print(math.gcd(*[x for x, y in coords]))
    print(math.gcd(*[y for x, y in coords]))
    return outline(instrs)


# TODO: Forget arrays, hashmaps, etc. We will have to work with the vertices & edges directly.
# For every scanline (y), determine the edges that go through that scanline, and do standard
# scanline fill.
def prob_2(data: list[str]):
    instrs = [
        (int(color[2:7], 16), dirs_ordered[int(color[7])])
        for _, _, color in [line.split() for line in data]
    ]
    loc = (0, 0)
    coords = [loc]
    for num, dr in instrs:
        loc = (loc[0] + dirs[dr][0] * num, loc[1] + dirs[dr][1] * num)
        coords.append(loc)
    print(math.gcd(*[x for x, y in coords[1:]]))
    print(math.gcd(*[y for x, y in coords[1:]]))
    return outline(instrs)


def main():
    with open(INPUT or "input.txt", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    start = time.perf_counter()
    result = prob_1(data) if PART == 1 else prob_2(data)
    elapsed = time.perf_counter() - start

    print(f"Problem {PART}: {result}")
    print(f"Time: {elapsed} s")


if __name__ == "__main__":
    main()
