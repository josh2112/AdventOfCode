#!/usr/bin/env python3

import time

# https://adventofcode.com/2023/day/16

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1

refl = {
    "/": {(1, 0): (0, -1), (-1, 0): (0, 1), (0, 1): (-1, 0), (0, -1): (1, 0)},
    "\\": {(1, 0): (0, 1), (-1, 0): (0, -1), (0, 1): (1, 0), (0, -1): (-1, 0)},
}


class Prob1:
    def __init__(self, data: list[str]):
        self.grid = [["X"] + [g for g in line] + ["X"] for line in data]
        self.grid.insert(0, ["X"] * len(self.grid[0]))
        self.grid.append(["X"] * len(self.grid[0]))
        self.energized = set()
        # self.limit = 999

    def solve(self):
        loc, vec = (0, 1), (1, 0)
        # self.energized.add((loc, vec))
        self.project(loc, vec, 0)
        return len(set(loc for loc, _ in self.energized))

    def project(self, loc, vec, i):
        while True:
            loc = (loc[0] + vec[0], loc[1] + vec[1])
            i += 1
            # if i >= self.limit:
            #    return
            # print(loc)
            g = self.grid[loc[1]][loc[0]]
            if g == "X" or (loc, vec) in self.energized:
                return
            self.energized.add((loc, vec))
            if g == "-" and vec[1] != 0:
                vec = (-1, 0)
                self.project(loc, (1, 0), i)
            elif g == "|" and vec[0] != 0:
                vec = (0, -1)
                self.project(loc, (0, 1), i)
            elif g == "\\" or g == "/":
                vec = refl[g][vec]

    def print_energized(self):
        g = [
            ["." for _ in range(len(self.grid[0]) - 2)]
            for _ in range(len(self.grid) - 2)
        ]
        for pt in set((loc[0] - 1, loc[1] - 1) for loc, _ in self.energized):
            g[pt[1]][pt[0]] = "#"
        for line in g:
            print("".join(line))


def prob_1(data: list[str]):
    p = Prob1(data)
    solution = p.solve()
    # p.print_energized()
    return solution


# Start from ANY edge, heading inward (corners can be either direction),
# find the most tiles that can be energized.
# Note: project(loc,vec) should return the number of tiles it will eventually energize.
# Must keep its own copy of self.energized?
def prob_2(data: list[str]):
    print(data)


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
