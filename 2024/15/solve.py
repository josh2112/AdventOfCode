"""https://adventofcode.com/2024/day/15"""

import argparse
import time
from collections import defaultdict

# Input file path (default is "input.txt")
INPUT = "input.ex3.txt"

# Part to solve, 1 or 2
PART = 2

DIRS = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)}


def push_1(grid, bot, d):
    # When up against a box, first figure out if we can push it or not -- is there an empty space
    # between it and the wall?
    stack = [(bot[0] + d[0], bot[1] + d[1])]
    while grid[stack[-1][1]][stack[-1][0]] == "O":
        stack.append((stack[-1][0] + d[0], stack[-1][1] + d[1]))
    # If so, move the bot and every box up to that empty space.
    if grid[stack[-1][1]][stack[-1][0]] == ".":
        for p in list(reversed(stack)):
            grid[p[1]][p[0]] = grid[p[1] - d[1]][p[0] - d[0]]
        grid[bot[1]][bot[0]] = "."
        return stack[0]
    else:
        return bot


def prob_1(data: list[str]) -> int:
    sep = data.index("")
    bot = None
    for y, line in enumerate(data[:sep]):
        data[y] = list(line)
        if not bot:
            for x, c in enumerate(line):
                if c == "@":
                    bot = (x, y)
    grid, moves = data[:sep], "".join(data[sep + 1 :])
    for m in moves:
        d = DIRS[m]
        if grid[bot[1] + d[1]][bot[0] + d[0]] != "#":
            bot = push_1(grid, bot, d)
    boxrows = [
        [(x, y) for x, c in enumerate(line) if c == "O"] for y, line in enumerate(grid)
    ]
    return sum(x + 100 * y for row in boxrows for x, y in row)


def flatten_to_set(gen):
    return set(x for i in list(gen) for x in i)


class Grid:
    def __init__(self, data):
        sep = data.index("")
        self.grid, self.bot, self.moves = (
            defaultdict(lambda: "."),
            None,
            "".join(data[sep + 1 :]),
        )
        self.w, self.h = len(data[0]) * 2, sep
        for y, line in enumerate(data[:sep]):
            for x, c in enumerate(line):
                if c == "#":
                    self.grid[(x * 2, y)], self.grid[(x * 2 + 1, y)] = "##"
                elif c == "O":
                    self.grid[(x * 2, y)], self.grid[(x * 2 + 1, y)] = "[]"
                elif c == "@":
                    self.bot = (x * 2, y)

    def __str__(self) -> str:
        g = [["."] * self.w for i in range(self.h)]
        for (x, y), t in self.grid.items():
            if t in "#[]":
                g[y][x] = t
        g[self.bot[1]][self.bot[0]] = "@"
        return "\n".join("".join(line) for line in g)

    def push_horiz(self, d):
        stack = []
        nxt = (self.bot[0] + d[0], self.bot[1] + d[1])
        while self.grid[nxt] in "[]":
            stack.append(nxt)
            nxt = (nxt[0] + d[0], nxt[1] + d[1])
        # If so, move the bot and every box up to that empty space.
        if self.grid[nxt] == ".":
            for p in [nxt] + list(reversed(stack)):
                self.grid[p] = self.grid[(p[0] - d[0], p[1] - d[1])]
            if stack:
                self.grid[stack[0]] = "."
            self.bot = (self.bot[0] + d[0], self.bot[1] + d[1])

    def box_at(self, p):
        if self.grid[p] == "[":
            return p, (p[0] + 1, p[1])
        elif self.grid[p] == "]":
            return p, (p[0] - 1, p[1])
        else:
            return ()

    def push_vert(self, d):
        # Going up/down is harder... a box is 2 wide and may affect 2 boxes above or below it.
        # This time the "stack" is the set of box coords on each row affected by the boxes in the
        # preceding row
        stack = []
        # Coords of boxes that will be pushed
        box_idxes_in_next_row = flatten_to_set(
            self.box_at(p) for p in [(self.bot[0] + d[0], self.bot[1] + d[1])]
        )
        while box_idxes_in_next_row:
            next_row_coords = [(x + d[0], y + d[1]) for x, y in box_idxes_in_next_row]
            # If any of these boxes are up against a wall, stop
            if any(self.grid[(x, y)] == "#" for x, y in next_row_coords):
                return
            stack.append(box_idxes_in_next_row)
            # Coords of boxes that will be pushed by these boxes
            box_idxes_in_next_row = flatten_to_set(
                self.box_at(p) for p in next_row_coords
            )

        next_row_coords = [(x + d[0], y + d[1]) for x, y in box_idxes_in_next_row]
        if not stack:
            self.bot = (self.bot[0] + d[0], self.bot[1] + d[1])
            return

        if any(self.grid[p] == "#" for p in next_row_coords):
            return

        self.bot = (self.bot[0] + d[0], self.bot[1] + d[1])
        for coords in list(reversed(stack)):
            for p in coords:
                self.grid[(p[0] + d[0], p[1] + d[1])] = self.grid[p]
                self.grid[p] = "."
        # for p in stack[0]:
        #    del self.grid[p]


def prob_2(data: list[str]) -> int:
    grid = Grid(data)
    for i, m in enumerate(grid.moves):
        d = DIRS[m]
        if grid.grid[(grid.bot[0] + d[0], grid.bot[1] + d[1])] != "#":
            if d[0] == 0:
                grid.push_vert(d)
            else:
                grid.push_horiz(d)

    return sum(x + 100 * y for (x, y), t in grid.grid.items() if t == "[")


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2024 day 15.")
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
