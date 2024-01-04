#!/usr/bin/env python3

from collections import defaultdict
import functools
import dataclasses
import time
from PIL import Image

# https://adventofcode.com/2023/day/21

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


@dataclasses.dataclass(frozen=True)
class Garden:
    xmax: int
    ymax: int
    rocks: frozenset[tuple[int, int]]
    start: tuple[int, int]

    @staticmethod
    def parse(data: list[str]):
        rocks = set()
        start = (0, 0)
        for y, line in enumerate(data):
            for x, c in enumerate(line):
                if c == "#":
                    rocks.add((x, y))
                elif c == "S":
                    start = (x, y)
        return Garden(len(data[0]), len(data), frozenset(rocks), start)

    @functools.cache
    def neighbors_1(self, u: tuple[int, int]):
        coords = set()
        for v in (
            (u[0] - 1, u[1]),
            (u[0], u[1] - 1),
            (u[0] + 1, u[1]),
            (u[0], u[1] + 1),
        ):
            if (
                v[0] >= 0
                and v[0] < self.xmax
                and v[1] >= 0
                and v[1] < self.ymax
                and v not in self.rocks
            ):
                coords.add(v)
        return coords

    @functools.cache
    def neighbors_2(self, u: tuple[int, int]):
        coords = defaultdict(set)
        for v in (
            (u[0] - 1, u[1]),
            (u[0], u[1] - 1),
            (u[0] + 1, u[1]),
            (u[0], u[1] + 1),
        ):
            vnorm = (v[0] % self.xmax, v[1] % self.ymax)
            if vnorm not in self.rocks:
                coords[(v[0] // self.xmax, v[1] // self.ymax)].add(vnorm)
        return coords


def save_img(path: str, g: Garden, coords: set[tuple[int, int]]):
    img = Image.new(mode="RGB", size=(g.xmax, g.ymax))
    for rock in g.rocks:
        img.putpixel(rock, (128, 128, 128))
    for coord in coords:
        img.putpixel(coord, (0, 255, 85))
    img.save(path, format="PNG")


def prob_1(data: list[str]):
    g = Garden.parse(data)
    stack = set([g.start])

    for i in range(64):
        newstack = set()
        for u in stack:
            newstack.update(g.neighbors_1(u))
        stack = newstack
        print(f"{i+1}: {len(stack)}")

    return len(stack)


# So the input grid is 131x131, with the start position at 65x65. This means there are 65 cells
# on all sides of the input. There are also no rocks in the center row or column, meaning the
# diamond can grow unobstructed in all 4 directions in the center column.
#
# The input step count is 26501365. After 65 to the edge, that leaves 26501300, which is evenly
# divisible by 131 (result 202300). So the walk extends to each border of the center, then goes out
# 202300 more 'plots' in all four directions.
#
# This also puts the frontier in each 'plot' right in the middle of the big diamond-shaped "valley"
#
def prob_2(data: list[str]):
    g = Garden.parse(data)
    stack = defaultdict(set)
    stack[(0, 0)].add(g.start)

    for i in range(20):
        newstack = defaultdict(set)
        for grid, coords in stack.items():
            for c in coords:
                newstack.update(g.neighbors_2(c))
        stack = newstack
        print(f"{i+1}: {[len(stack[g]) for g in stack]}")

    return len(stack)


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
