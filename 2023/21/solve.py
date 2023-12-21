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

    @functools.cache
    def neighbors(self, u: tuple[int, int], bounds_check: bool = False):
        coords = set()
        for v in (
            (u[0] - 1, u[1]),
            (u[0], u[1] - 1),
            (u[0] + 1, u[1]),
            (u[0], u[1] + 1),
        ):
            if (
                not bounds_check
                or (v[0] >= 0 and v[0] < self.xmax and v[1] >= 0 and v[1] < self.ymax)
            ) and (v[0] % self.xmax, v[1] % self.ymax) not in self.rocks:
                coords.add(v)
        return coords


@dataclasses.dataclass
class GIFBuilder:
    g: Garden
    path: str
    imgs = []

    def add_img(self, coords: set[tuple[int, int]]):
        img = Image.new(mode="RGB", size=(self.g.xmax, self.g.ymax))
        for rock in self.g.rocks:
            img.putpixel(rock, (128, 128, 128))
        for coord in coords:
            img.putpixel(coord, (0, 255, 85))

        self.imgs.append(img)

    def save(self, length: float):
        self.imgs[0].save(
            self.path,
            format="GIF",
            append_images=self.imgs[1:],
            save_all=True,
            duration=length,
        )


def prob_2(data: list[str]):
    g = Garden.parse(data)
    stack = set([g.start])
    gifbuilder = GIFBuilder(g, "prob2.gif")

    for i in range(500):
        newstack = set()
        for u in stack:
            newstack.update(g.neighbors(u, bounds_check=True))
        stack = newstack
        print(f"{i+1}: {len(stack)}")
        gifbuilder.add_img(stack)

    gifbuilder.save(i)
    return len(stack)


def prob_1(data: list[str]):
    g = Garden.parse(data)
    stack = set([g.start])

    for i in range(64):
        newstack = set()
        for u in stack:
            newstack.update(g.neighbors(u, bounds_check=True))
        stack = newstack
        print(f"{i+1}: {len(stack)}")

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
