"""https://adventofcode.com/2023/day/16"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 2

refl = {
    "/": {(1, 0): (0, -1), (-1, 0): (0, 1), (0, 1): (-1, 0), (0, -1): (1, 0)},
    "\\": {(1, 0): (0, 1), (-1, 0): (0, -1), (0, 1): (1, 0), (0, -1): (-1, 0)},
}


class Prob1:
    def __init__(self, grid: list[list[str]]):
        self.grid = grid
        self.energized = set()
        # self.limit = 999

    def solve(self, loc, vec):
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
    grid = [["X"] + [g for g in line] + ["X"] for line in data]
    grid.insert(0, ["X"] * len(grid[0]))
    grid.append(["X"] * len(grid[0]))

    return Prob1(grid).solve((0, 1), (1, 0))


# Start from ANY edge, heading inward (corners can be either direction),
# find the most tiles that can be energized.
# Note: project(loc,vec) should return the number of tiles it will eventually energize.
# Must keep its own copy of self.energized?
def prob_2(data: list[str]):
    grid = [["X"] + [g for g in line] + ["X"] for line in data]
    grid.insert(0, ["X"] * len(grid[0]))
    grid.append(["X"] * len(grid[0]))

    max_sol = 0
    xmax = len(grid[0]) - 1
    ymax = len(grid) - 1
    for x in range(1, xmax - 1):
        max_sol = max(
            max_sol,
            Prob1(grid).solve((x, 0), (0, 1)),
            Prob1(grid).solve((x, ymax), (0, -1)),
        )
    for y in range(1, ymax - 1):
        max_sol = max(
            max_sol,
            Prob1(grid).solve((0, y), (1, 0)),
            Prob1(grid).solve((xmax, 0), (-1, 0)),
        )
    return max_sol


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2023 day 16.")
    parser.add_argument("-p", "--part", choices=("1", "2", "all"), default=str(PART))
    parser.add_argument("-i", "--input", default=INPUT)
    args = parser.parse_args()
    part, infile = args.part, args.input

    with open(infile, mode="r", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    start = time.perf_counter()
    if part in ("1", "all"):
        print(f"Part 1: {prob_1(data)}")
    if part in ("2", "all"):
        print(f"Part 2: {prob_2(data)}")

    elapsed = time.perf_counter() - start
    print(f"Time: {elapsed} s")

    return elapsed


if __name__ == "__main__":
    main()
