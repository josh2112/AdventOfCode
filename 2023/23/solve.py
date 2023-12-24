#!/usr/bin/env python3

import time

# https://adventofcode.com/2023/day/23

# Input file path (default is "input.txt")
INPUT = "input.ex2.txt"

# Part to solve, 1 or 2
PART = 1


def walk(path: list[tuple[int, int]], data: list[str], goal: tuple[int, int]):
    possibilities = []
    while True:
        for vec in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            loc = (path[-1][0] + vec[0], path[-1][1] + vec[1])
            nxt = data[loc[1]][loc[0]]
            if loc == goal:
                return len(path) + 1
            if loc not in path and (
                nxt == "."
                or (nxt == "^" and vec == (0, -1))
                or (nxt == ">" and vec == (1, 0))
                or (nxt == "v" and vec == (0, 1))
                or (nxt == "<" and vec == (-1, 0))
            ):
                possibilities.append(loc)
        if possibilities:
            path.append(possibilities[0])
            possibilities.clear()
        if len(possibilities) > 1:
            return max(walk(path + [p], data, goal) for p in possibilities[1:])


def prob_1(data: list[str]):
    path = [(1, 0), (1, 1)]
    goal = (len(data) - 1, len(data[0]) - 2)
    return walk(path, data, goal)


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
