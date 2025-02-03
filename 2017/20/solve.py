"""https://adventofcode.com/2017/day/20"""

import argparse
import math
import re
import time
from collections.abc import Generator
from dataclasses import dataclass, field
from itertools import combinations
from sys import maxsize

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 2


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Point(self.x * scalar, self.y * scalar, self.z * scalar)

    def __truediv__(self, scalar):
        return Point(self.x / scalar, self.y / scalar, self.z / scalar)

    def dist(self):
        return abs(self.x) + abs(self.y) + abs(self.z)


@dataclass
class Particle:
    i: int
    p: Point
    v: Point
    a: Point
    half_a: Point = field(init=False)
    v_plus_half_a: Point = field(init=False)

    def __post_init__(self):
        self.half_a = self.a / 2
        self.v_plus_half_a = self.v + self.half_a

    def project(self, t: int):
        # The formula for their wierd discrete equation of motion
        # (a0/2) * t^2 + (v0 + a0/2) * t + p
        return self.half_a * t * t + self.v_plus_half_a * t + self.p

    def intersects(self, other: "Particle") -> bool:
        # Find the interesection(s) of these 2 particles
        # First:
        #  self.half_a * t * t + self.v_plus_half_a * t + self.p =
        #   other.half_a * t * t + other.v_plus_half_a * t + other.p
        # Subtract right side from left side:
        # (self.half_a - other.half_a) * t * t + (self.v_plus_half_a-other.v_plus_half_a) * t + (self.p-other.p) = 0
        # Looking for the form a*t*t + b*t + c = 0, so
        a = self.half_a - other.half_a
        b = self.v_plus_half_a - other.v_plus_half_a
        c = self.p - other.p

        def solve_t(a, b, c):
            """Returns the positive roots of the quadratic equation with coefficients a, b and c.
            If no positive roots, returns None. If y == 0 for all t, returns maxsize"""
            # Is it quadratic (and does it have a solution?)
            if a != 0:
                if (discr := b * b - 4 * a * c) >= 0:
                    d_sq, ta = math.sqrt(discr), 2 * a
                    return [s for s in ((-b - d_sq) / ta, (-b + d_sq) / ta) if s >= 0]
            elif b != 0:  # Is it linear?
                return [-c / b] if -c / b >= 0 else []
            elif c == 0:
                # If a, b and c are all 0, the particles always conincide on this axis. Represent with maxsize
                return maxsize

            # No roots
            return None

        # Intersection times in each dimension (x,y and z). Each could be a list of 0 or more positive times,
        # None (representing no intersection), or maxsize (representing coincident at all times).
        t = [solve_t(a.x, b.x, c.x), solve_t(a.y, b.y, c.y), solve_t(a.z, b.z, c.z)]

        # End early if any axis doesn't interesect
        if any(x is None for x in t):
            return False

        # Remove axes where particles always coincide
        t = [i for i in t if i != maxsize]

        # Return True if there's a positive value in t that occurs in every tuple
        all_valid_t = set(x for p in t for x in p)
        return any(all(x in p for p in t) for x in all_valid_t)


def parse(data: list[str]) -> Generator[Particle]:
    for i, line in enumerate(data):
        vs = [int(v) for v in re.findall(r"(-?\d+)", line)]
        yield Particle(i, Point(*vs[0:3]), Point(*vs[3:6]), Point(*vs[6:9]))


def prob_1(data: list[str]) -> int:
    # Just pick an arbitrarily high time and find the closest particle to 0 at that time...
    return min(list(parse(data)), key=lambda p: p.project(1_000_000).dist()).i


def prob_2(data: list[str]) -> int:
    particles = list(parse(data))
    colliders = set()

    for p1, p2 in combinations(particles, r=2):
        if p1.intersects(p2):
            colliders.add(p1.i)
            colliders.add(p2.i)

    return len([p for p in particles if p.i not in colliders])


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
