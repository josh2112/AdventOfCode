#!/usr/bin/env python3

import time
import functools
from dataclasses import dataclass

# https://adventofcode.com/2023/day/18

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 2


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True)
class Edge:
    v0: Point
    v1: Point


def gen_edges(instrs: list[tuple[int, str]]):
    dirs = {"R": (1, 0), "U": (0, -1), "D": (0, 1), "L": (-1, 0)}
    loc = (0, 0)
    loc_prev = loc
    for num, dr in instrs:
        loc = (loc[0] + dirs[dr][0] * num, loc[1] + dirs[dr][1] * num)
        if dr in ("R", "D"):
            yield Edge(Point(*loc_prev), Point(*loc))
        else:
            yield Edge(Point(*loc), Point(*loc_prev))
        loc_prev = loc


# TODO: Think about how we can memoize. Obviously the scanline number can't be a dependency!
# This can't be memoized because it depends on y. But y is only necessary if there are
# horizontal edges.
def calc_scanline_volume(y: int, edges: list[Edge]) -> int:
    volume = 0
    last_vert = None
    last_edge = None
    inside = False

    for edge in edges:
        # print("----------------------")

        if edge.v0.y == edge.v1.y:
            # it's horizontal: add the length (excluding ends)
            volume += edge.v1.x - edge.v0.x - 1
            # print(f"Horizontal edge -- adding {edge.v1.x - edge.v0.x - 1}")
        else:
            # it's vertical
            volume += 1
            # print(f"Vertical edge -- adding 1")

            if last_edge and last_edge.v0.y == last_edge.v1.y:
                # Last edge was a horizontal, figure out whether inside/outside flipped...
                if (
                    min(last_vert.v0.y, last_vert.v1.y) < y
                    and min(edge.v0.y, edge.v1.y) < y
                ) or (
                    max(last_vert.v0.y, last_vert.v1.y) > y
                    and max(edge.v0.y, edge.v1.y) > y
                ):  # U-shaped (or inverse-U)
                    inside = not inside
                    # print(
                    #    f"It's U (or inverse U) shaped... now {'inside' if inside else 'outside'}"
                    # )

                # else:
                # print(f"It's N-shaped... now {'inside' if inside else 'outside'}")

            else:
                if inside:
                    volume += edge.v0.x - last_edge.v0.x - 1
                inside = not inside
            last_vert = edge
        last_edge = edge

    return volume


def calc_volume(instrs: list[tuple[int, str]]) -> int:
    edges = list(gen_edges(instrs))
    ymin = min(e.v0.y for e in edges)
    ymax = max(e.v1.y for e in edges)

    volume = 0
    for y in range(ymin, ymax + 1):
        volume += calc_scanline_volume(
            y,
            sorted(
                (e for e in edges if e.v0.y <= y <= e.v1.y),
                key=lambda e: e.v0.x + e.v1.x,
            ),
        )

    return volume


def prob_1(data: list[str]):
    return calc_volume(
        [(int(num), dr) for dr, num, _ in [line.split() for line in data]]
    )


def prob_2(data: list[str]):
    dirs_ordered = ["R", "D", "L", "U"]
    return calc_volume(
        [
            (int(color[2:7], 16), dirs_ordered[int(color[7])])
            for _, _, color in [line.split() for line in data]
        ]
    )


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
