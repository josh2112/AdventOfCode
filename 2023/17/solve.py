#!/usr/bin/env python3

import sys
import time

# https://adventofcode.com/2023/day/17

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def prob_1(data: list[str]):
    unvisited = [(x, y) for x in range(len(data)) for y in range(len(data[0]))]
    cost = [[sys.maxsize for _ in range(len(data[0]))] for _ in range(len(data))]
    cost[0][0] = 0
    nx, ny = 0, 0
    for x, y in [
        (nx - 1, ny - 1),
        (nx - 1, ny),
        (nx - 1, ny + 1),
        (nx + 1, ny - 1),
        (nx + 1, ny),
        (nx + 1, ny + 1),
        (nx, ny - 1),
        (nx, ny + 1),
    ]:
        if x < 0 or y < 0 or x >= range(len(data[0])) or y >= range(len(data)):
            continue
        cost[y][x] = min(cost[y][x], data[y][x] + cost[ny][nx])
    unvisited.remove((nx, ny))
    if nx == len(data[0]) - 1 and ny == len(data) - 1:
        break


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
