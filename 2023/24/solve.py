#!/usr/bin/env python3

import time
import re
import itertools

# https://adventofcode.com/2023/day/24

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


class Line:
    def __init__(self, nums):
        self.pt, self.vec = nums[:3], nums[3:]

    def __repr__(self) -> str:
        return f"{self.pt} @ {self.vec}"

    def intersect_2d(self, other: "Line"):
        a, b, c, d = self.pt[0], self.pt[1], self.vec[0], self.vec[1]
        e, f, g, h = other.pt[0], other.pt[1], other.vec[0], other.vec[1]
        det = d * g - c * h
        if not det:
            return None
        v = (c * (f - b) + d * (a - e)) / det
        u = (e + g * v - a) / c
        return None if u < 0 or v < 0 else (a + c * u, b + d * u)


def prob_1(data: list[str]):
    lines = [Line([int(d) for d in re.split("[,@]", line)]) for line in data]
    bounds = (7, 27) if "ex" in INPUT else (200000000000000, 400000000000000)

    cnt = 0
    for a, b in itertools.combinations(lines, 2):
        cross = a.intersect_2d(b)
        if not cross:
            pass  # print(f"{a} X {b}: past or none")
        elif (
            cross[0] >= bounds[0]
            and cross[0] <= bounds[1]
            and cross[1] >= bounds[0]
            and cross[1] <= bounds[1]
        ):
            cnt += 1
            # print(f"{a} X {b}: inside {cross}")
        else:
            pass  # print(f"{a} X {b}: outside {cross}")

    # 15939 too high?
    return cnt


def prob_2(data: list[str]):
    print(data)


def main():
    with open(INPUT or "input.txt", mode="r", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    start = time.perf_counter()
    result = prob_1(data) if PART == 1 else prob_2(data)
    elapsed = time.perf_counter() - start

    print(f"Problem {PART}: {result}")
    print(f"Time: {elapsed} s")


if __name__ == "__main__":
    main()
