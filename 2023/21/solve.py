#!/usr/bin/env python3

import functools
import dataclasses
import time
from PIL import Image

# https://adventofcode.com/2023/day/21

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 2


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

    def tiled(self, size: int):
        rocks = []
        for x in range(size):
            for y in range(size):
                rocks.extend(
                    (r[0] + self.xmax * x, r[1] + self.ymax * y) for r in self.rocks
                )

        return Garden(
            self.xmax * size,
            self.ymax * size,
            frozenset(rocks),
            (
                self.xmax * (size // 2) + self.start[0],
                self.ymax * (size // 2) + self.start[1],
            ),
        )

    @functools.cache
    def neighbors(self, u: tuple[int, int]):
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


def show_img(path: str, g: Garden, coords: set[tuple[int, int]]):
    img = Image.new(mode="RGB", size=(g.xmax, g.ymax))
    for rock in g.rocks:
        img.putpixel(rock, (128, 128, 128))
    for coord in coords:
        img.putpixel(coord, (0, 255, 85))
    img.save(path, format="PNG")
    img.show()


def prob_1(data: list[str]):
    g = Garden.parse(data)
    stack = set([g.start])

    for i in range(64):
        newstack = set()
        for u in stack:
            newstack.update(g.neighbors(u))
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
# It ends up making a giant multi-plot diamond. The plots are pretty regular -- there's a plot
# representing each "point", two alternating plots that make up each edge, and 2 alternating center
# plots. We just have to make the smallest multi-plot diamond we can to get all the various tile
# plot counts, figure out how many of each there would be in a 202300-radius multi-plot diamond,
# then add them all up.
def prob_2(data: list[str]):
    width = 5

    g = Garden.parse(data)
    plotsize = g.xmax

    g = g.tiled(width)
    tiles: set[tuple[int, int]] = set([g.start])

    for _ in range(plotsize * (width // 2) + 65):
        next_tiles = set()
        for u in tiles:
            next_tiles.update(g.neighbors(u))
        tiles = next_tiles

    def count_tiles_in_plot(xy: tuple[int, int]):
        x0, x1 = xy[0] * plotsize, (xy[0] + 1) * plotsize
        y0, y1 = xy[1] * plotsize, (xy[1] + 1) * plotsize
        return sum(1 for t in tiles if x0 <= t[0] < x1 and y0 <= t[1] < y1)

    half = width // 2

    t, l, r, b = map(
        count_tiles_in_plot,
        ((half, 0), (0, half), (width - 1, half), (half, width - 1)),
    )
    lto, rto, lbo, rbo = map(
        count_tiles_in_plot,
        ((half - 1, 0), (half + 1, 0), (half - 1, width - 1), (half + 1, width - 1)),
    )
    lti, rti, lbi, rbi = map(
        count_tiles_in_plot,
        ((half - 1, 1), (half + 1, 1), (half - 1, width - 2), (half + 1, width - 2)),
    )
    m1, m2 = map(count_tiles_in_plot, ((half, 1), (half, 2)))

    # t, l, r, b, lto, rto, lbo, rbo, lti, rti, lbi, rbi, m1, m2
    # 5515 5479 5508 5472 935 909 944 902 6384 6393 6357 6377 7232 7262

    half = (26501365 - 65) / 131

    return (
        t
        + l
        + r
        + b
        + half * (lto + rto + lbo + rbo)
        + (half - 1) * (lti + rti + lbi + rbi)
        + pow(half, 2) * m1
        + pow((half - 1), 2) * m2
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
