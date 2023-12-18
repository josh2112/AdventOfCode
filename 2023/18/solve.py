#!/usr/bin/env python3

import time
from dataclasses import dataclass

# https://adventofcode.com/2023/day/18

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1

dirs = {"R": (1, 0), "U": (0, -1), "D": (0, 1), "L": (-1, 0)}
dirs_ordered = ["R", "D", "L", "U"]


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True)
class Edge:
    v0: Point
    v1: Point


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


def gen_edges(instrs: list[tuple[int, str]]):
    loc = (0, 0)
    loc_prev = loc
    for num, dr in instrs:
        loc = (loc[0] + dirs[dr][0] * num, loc[1] + dirs[dr][1] * num)
        if dr in ("R", "D"):
            yield Edge(Point(*loc_prev), Point(*loc))
        else:
            yield Edge(Point(*loc), Point(*loc_prev))
        loc_prev = loc


# TODO: Still doesn't work for scanline 12 of input.txt part 1...
def calc_scanline_volume(y: int, edges: list[Edge]) -> int:
    volume = 0
    last_vert = None
    last_edge = None
    inside = False
    for edge in edges:
        if edge.v0.y == edge.v1.y:
            # it's horizontal: count the inner length
            volume += edge.v1.x - edge.v0.x - 1
        else:
            # it's vertical
            volume += 1

            if last_edge and last_edge.v0.y == last_edge.v1.y:
                # Last edge was a horizontal, figure out whether inside outside flipped...
                last_y_min = min(last_edge.v0.y, last_edge.v1.y)
                y_min = min(edge.v0.y, edge.v1.y)
                if (last_y_min < y and y_min < y) or (
                    last_y_min > y and y_min > y
                ):  # U-shaped
                    inside = not inside
            else:
                if inside:
                    # Space is only inside if last edge was not a horizontal!
                    volume += edge.v0.x - last_vert.v0.x - 1
                inside = not inside
            last_vert = edge
        last_edge = edge

    print(volume)
    return volume


def prob_1(data: list[str]):
    instrs = [(int(num), dr) for dr, num, _ in [line.split() for line in data]]
    vol1 = outline(instrs)

    edges = list(gen_edges(instrs))
    # print(edges)
    ymin = min(e.v0.y for e in edges)
    ymax = max(e.v1.y for e in edges)

    vol2 = 0
    for y in range(ymin, ymax + 1):
        vol2 += calc_scanline_volume(
            y,
            sorted(
                (e for e in edges if e.v0.y <= y <= e.v1.y),
                key=lambda e: e.v0.x + e.v1.x,
            ),
        )

    return vol1, vol2


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
