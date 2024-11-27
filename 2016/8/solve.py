"""https://adventofcode.com/2016/day/8"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.ex.txt"

# Part to solve, 1 or 2
PART = 1


def print_grid(grid: list[list[str]]):
    for line in grid:
        print("".join(line))


def do_grid(data: list[str]):
    w, h = 50, 6  # 7x3 for examples
    grid = [(["."] * w) for a in range(h)]
    for line in data:
        if line[1] == "e":
            rect = [int(v) for v in line.split()[-1].split("x")]
            for r in range(rect[1]):
                for c in range(rect[0]):
                    grid[r][c] = "#"
        else:
            tk = line.replace("=", " ").split()
            i, amt = int(tk[-3]), int(tk[-1])
            if line[7] == "r":
                orig = grid[i].copy()
                for c in range(len(grid[i])):
                    grid[i][(c + amt) % len(grid[i])] = orig[c]
            else:
                orig = [grid[r][i] for r in range(len(grid))]
                for r in range(len(grid)):
                    grid[(r + amt) % len(grid)][i] = orig[r]
    return grid


def prob_1(data: list[str]) -> int:
    grid = do_grid(data)
    return sum(
        sum(1 if grid[r][c] == "#" else 0 for c in range(len(grid[r])))
        for r in range(len(grid))
    )


def prob_2(data: list[str]) -> int:
    grid = do_grid(data)
    print_grid(grid)
    return 0


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2016 day 8.")
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
