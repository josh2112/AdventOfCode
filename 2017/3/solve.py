"""https://adventofcode.com/2017/day/3"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1

DIRS = ((1, 0), (0, -1), (-1, 0), (0, 1))
DIAGS = ((-1, -1), (1, -1), (-1, 1), (1, 1))


def gen_sides():
    i = 2
    while True:
        yield i // 2
        i += 1


def gen_dirs():
    d = 0
    while True:
        yield DIRS[d]
        d = (d + 1) % len(DIRS)


def gen_neighbors(p: tuple[int, int]):
    for dx in DIRS + DIAGS:
        yield (p[0] + dx[0], p[1] + dx[1])


def coord_of(num: int) -> tuple[int, int]:
    """Returns (x,y) of cell with the given num"""
    s, d = gen_sides(), gen_dirs()
    a, p = 1, (0, 0)
    while True:
        nd = next(d)
        for i in range(next(s)):
            p = (p[0] + nd[0], p[1] + nd[1])
            if (a := a + 1) == num:
                return p


def fill(num: int) -> tuple[int, int]:
    """Returns first cell value larger than the given number"""
    s, d = gen_sides(), gen_dirs()
    p = (0, 0)
    grid = {p: 1}
    while True:
        nd = next(d)
        for i in range(next(s)):
            p = (p[0] + nd[0], p[1] + nd[1])
            a = sum(grid[px] if px in grid else 0 for px in gen_neighbors(p))
            if a > num:
                return a
            else:
                grid[p] = a


def prob_1(data: list[str]) -> int:
    return sum(abs(x) for x in coord_of(int(data[0])))


def prob_2(data: list[str]) -> int:
    return fill(int(data[0]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solves AoC 2017 day 3.")
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
