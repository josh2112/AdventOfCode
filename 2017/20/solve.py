"""https://adventofcode.com/2017/day/20"""

import argparse
import re
import time
from dataclasses import dataclass

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


@dataclass
class Point:
    x: int
    y: int
    z: int


@dataclass
class Particle:
    i: int
    p: Point
    v: Point
    a: Point

    def update(self):
        self.v = Point(self.v.x + self.a.x, self.v.y + self.a.y, self.v.z + self.a.z)
        self.p = Point(self.v.x + self.p.x, self.v.y + self.p.y, self.v.z + self.p.z)
        return abs(self.p.x) + abs(self.p.y) + abs(self.p.z)


def parse(data: list[str]) -> int:
    for i, line in enumerate(data):
        vs = [int(v) for v in re.findall(r"(-?\d+)", line)]
        yield Particle(i, Point(*vs[0:3]), Point(*vs[3:6]), Point(*vs[6:9]))


def dist(p: Particle):
    return abs(p.p.x) + abs(p.p.y) + abs(p.p.z)


def prob_1(data: list[str]) -> int:
    particles = list(parse(data))
    closest = particles[0]
    for t in range(1_000):
        if (c := min(particles, key=lambda p: p.update())) != closest:
            closest = c
    return closest.i


def prob_2(data: list[str]) -> int:
    particles = list(parse(data))
    for t in range(1_000):
        pos = {p: p.update() for p in particles}
        if (c := min(particles, key=lambda p: p.update())) != closest:
            closest = c
    return closest.i


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solves AoC 2017 day 20.")
    parser.add_argument("-p", "--part", choices=("1", "2", "all"), default=str(PART))
    parser.add_argument("-i", "--input", default=INPUT)
    args = parser.parse_args()

    with open(args.input, mode="r", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    start = time.perf_counter()
    if args.part in ("1", "all"):
        print(f"Part 1: {prob_1(data)}")
    if args.part in ("2", "all"):
        print(f"Part 2: {prob_2(data)}")

    print(f"Time: {time.perf_counter() - start} s")
