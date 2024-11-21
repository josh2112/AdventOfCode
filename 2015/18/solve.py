"""https://adventofcode.com/2015/day/18"""

import argparse
import time
from itertools import product

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1

SURROUNDING = set(product((-1, 0, 1), repeat=2)).difference(((0, 0),))


def parse(data: list[str]) -> dict[(int, int), bool]:
    grid: dict[(int, int), bool] = {}
    for y in range(len(data)):
        for x in range(len(data[0])):
            grid[(x, y)] = data[y][x] == "#"
    return grid, (
        max(k[0] for k in grid.keys()) + 1,
        max(k[1] for k in grid.keys()) + 1,
    )


def print_grid(grid: dict[(int, int), bool], size: tuple[int, int]):
    print("-" * (size[1]))
    for y in range(size[1]):
        print("".join("#" if grid.get((x, y), False) else "." for x in range(size[0])))
    print("-" * size[1])


def iterate(
    grid: dict[(int, int), bool], size: tuple[int, int], keep_corners: bool = False
):
    to_flip = []
    for y in range(size[1]):
        for x in range(size[0]):
            is_lit = grid.get((x, y), False)
            num_lit_neighbors = sum(
                1 if grid.get((x + p[0], y + p[1]), False) else 0 for p in SURROUNDING
            )
            if is_lit != (is_lit and num_lit_neighbors in (2, 3)) or (
                not is_lit and num_lit_neighbors == 3
            ):
                to_flip.append((x, y))
    for pt in to_flip:
        grid[pt] = not grid[pt]
    if keep_corners:
        for pt in (
            (0, 0),
            (size[0] - 1, 0),
            (0, size[1] - 1),
            (size[0] - 1, size[1] - 1),
        ):
            grid[pt] = True


def prob_1(data: list[str]) -> int:
    grid, size = parse(data)
    # print_grid(grid, size)

    for i in range(4 if size[0] == 6 else 100):
        iterate(grid, size)
        # print_grid(grid, size)

    return sum(
        sum(1 if grid.get((x, y), False) else 0 for x in range(size[0]))
        for y in range(size[1])
    )


def prob_2(data: list[str]) -> int:
    grid, size = parse(data)
    # print_grid(grid, size)

    for i in range(5 if size[0] == 6 else 100):
        iterate(grid, size, keep_corners=True)
        # print_grid(grid, size)

    return sum(
        sum(1 if grid.get((x, y), False) else 0 for x in range(size[0]))
        for y in range(size[1])
    )
    return 0


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2015 day 18.")
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
