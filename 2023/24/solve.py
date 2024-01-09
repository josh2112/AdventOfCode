#!/usr/bin/env python3

import random
import time
import re
import itertools

# https://adventofcode.com/2023/day/24

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 2


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


class GaussianElimination:
    def __init__(self, matrix: list[list[float]]):
        self.matrix = matrix

    def __str__(self) -> str:
        return "\n".join("".join(f"{i:5}" for i in row) for row in self.matrix)

    def solve(self) -> list[float]:
        # Using the xth row, eliminate the xth variable from all following rows.
        m = self.matrix
        for i in range(0, len(m) - 1):
            for r in range(i + 1, len(m)):
                print(f"Using row {i}, eliminate {i}th var from row {r}:")
                s = -m[r][i] / m[i][i]
                for j in range(0, len(m[r])):
                    m[r][j] += s * m[i][j]

        if all(i == 0 for i in m[-1][:-1]):
            raise Exception("Dependent system, no solution")

        v: list[float] = [0] * len(m)

        for i in range(len(v) - 1, -1, -1):
            for j in range(i + 1, len(m)):
                m[i][-1] -= m[i][j] * v[j]
            v[i] = m[i][len(v)] / m[i][i]

        return v


def prob_1(data: list[str]):
    lines = [Line([int(d) for d in re.split("[,@]", line)]) for line in data]
    bounds = (7, 27) if "ex" in INPUT else (200000000000000, 400000000000000)

    cnt = 0
    for a, b in itertools.combinations(lines, 2):
        cross = a.intersect_2d(b)
        if not cross:
            pass
        elif (
            cross[0] >= bounds[0]
            and cross[0] <= bounds[1]
            and cross[1] >= bounds[0]
            and cross[1] <= bounds[1]
        ):
            cnt += 1

    return cnt


def eq_xyz(l0: Line, l1: Line):
    x0, y0, z0 = l0.pt
    dx0, dy0, dz0 = l0.vec
    x1, y1, z1 = l1.pt
    dx1, dy1, dz1 = l1.vec

    return [
        [
            dy0 - dy1,
            dx1 - dx0,
            0,
            y1 - y0,
            x0 - x1,
            0,
            x0 * dy0 - y0 * dx0 - x1 * dy1 + y1 * dx1,
        ],
        [
            dz0 - dz1,
            0,
            dx1 - dx0,
            z1 - z0,
            0,
            x0 - x1,
            x0 * dz0 - z0 * dx0 - x1 * dz1 + z1 * dx1,
        ],
        [
            0,
            dz0 - dz1,
            dy1 - dy0,
            0,
            z1 - z0,
            y0 - y1,
            y0 * dz0 - z0 * dy0 - y1 * dz1 + z1 * dy1,
        ],
    ]


def prob_2(data: list[str]):
    all_lines = [Line([int(d) for d in re.split("[,@]", line)]) for line in data]
    lines = random.choices(all_lines, k=3)

    # a, b, c, da, db, dc
    system = eq_xyz(lines[0], lines[1])
    system.extend(eq_xyz(lines[1], lines[2]))
    g = GaussianElimination(system).solve()
    return g


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
