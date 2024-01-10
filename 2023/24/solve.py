"""https://adventofcode.com/2023/day/24"""

import argparse
from fractions import Fraction as fr
import itertools
import random
import re
import time

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
    def __init__(self, matrix: list[list[fr]]):
        self.matrix = matrix

    def __str__(self) -> str:
        return "\n".join("".join(f"{i:5}" for i in row) for row in self.matrix)

    def solve(self) -> list[fr]:
        # Using the xth row, eliminate the xth variable from all following rows.
        m = self.matrix
        for i in range(0, len(m) - 1):
            for r in range(i + 1, len(m)):
                if m[i][i] == 0:
                    # Pivot element is zero. Swap with first row that is nonzero here.
                    j = next(j for j in range(i + 1, len(m)) if m[j][i] != 0)
                    # print(f"Swap rows {i+1} and {j+1}")
                    tmp = m[j]
                    m[j] = m[i]
                    m[i] = tmp
                else:
                    s = -m[r][i] / m[i][i]
                    # print(f"Add row {i+1} * {s} to row {r+1}:")
                    for j in range(0, len(m[r])):
                        m[r][j] += s * m[i][j]

        if all(i == 0 for i in m[-1][:-1]):
            raise ArithmeticError("Dependent system, no solution")

        v: list[fr] = [fr(0)] * len(m)

        for i in range(len(v) - 1, -1, -1):
            for j in range(i + 1, len(m)):
                m[i][-1] -= m[i][j] * v[j]
            v[i] = m[i][len(v)] / m[i][i]

        return v


def prob_1(data: list[str], is_example: bool ):
    lines = [Line([int(d) for d in re.split("[,@]", line)]) for line in data]
    bounds = (7, 27) if is_example else (200000000000000, 400000000000000)

    cnt = 0
    for a, b in itertools.combinations(lines, 2):
        if (cross := a.intersect_2d(b)) and (
            (bounds[0] <= cross[0] <= bounds[1])
            and (bounds[0] <= cross[1] <= bounds[1])
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
            fr(dy0 - dy1),
            fr(dx1 - dx0),
            fr(0),
            fr(y1 - y0),
            fr(x0 - x1),
            fr(0),
            fr(x0 * dy0 - y0 * dx0 - x1 * dy1 + y1 * dx1),
        ],
        [
            fr(dz0 - dz1),
            fr(0),
            fr(dx1 - dx0),
            fr(z1 - z0),
            fr(0),
            fr(x0 - x1),
            fr(x0 * dz0 - z0 * dx0 - x1 * dz1 + z1 * dx1),
        ],
        [
            fr(0),
            fr(dz0 - dz1),
            fr(dy1 - dy0),
            fr(0),
            fr(z1 - z0),
            fr(y0 - y1),
            fr(y0 * dz0 - z0 * dy0 - y1 * dz1 + z1 * dy1),
        ],
    ]


def prob_2(data: list[str]):
    all_lines = [Line([int(d) for d in re.split("[,@]", line)]) for line in data]
    lines = random.choices(all_lines, k=3)

    # a, b, c, da, db, dc
    system = eq_xyz(lines[0], lines[1])
    system.extend(eq_xyz(lines[1], lines[2]))
    r = GaussianElimination(system).solve()
    print(f"{r[0]}, {r[1]}, {r[2]} @ {r[3]}, {r[4]}, {r[5]}")
    return round(r[0] + r[1] + r[2], 10)


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2023 day 24.")
    parser.add_argument("-p", "--part", choices=("1", "2", "all"), default=str(PART))
    parser.add_argument("-i", "--input", default=INPUT)
    args = parser.parse_args()
    part, infile = args.part, args.input

    with open(infile, mode="r", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    start = time.perf_counter()
    if part in ("1", "all"):
        print(f"Part 1: {prob_1(data, "ex" in infile)}")
    if part in ("2", "all"):
        print(f"Part 2: {prob_2(data)}")

    elapsed = time.perf_counter() - start
    print(f"Time: {elapsed} s")

    return elapsed


if __name__ == "__main__":
    main()
