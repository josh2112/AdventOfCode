#!/usr/bin/env python3

import time

# https://adventofcode.com/2023/day/10

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 2


def prob_1(data: list[str]):
    LEFT, RIGHT, DOWN, UP = (-1, 0), (1, 0), (0, 1), (0, -1)
    d = [[c for c in line] for line in data]
    ispipe = [[False for c in line] for line in data]
    ystart = next(y for y, line in enumerate(d) if "S" in line)
    xstart = d[ystart].index("S")
    x, y, dist = xstart, ystart, 0

    if d[y][x + 1] in "J7-":
        vec = RIGHT
    elif d[y][x - 1] in "FL":
        vec = LEFT
    else:
        vec = UP

    ispipe[y][x] = True
    x += vec[0]
    y += vec[1]
    dist += 1

    while x != xstart or y != ystart:
        if d[y][x] == "L":  # down -> right, left -> up
            vec = UP if vec == LEFT else RIGHT
        elif d[y][x] == "J":  # right -> up, down -> left
            vec = UP if vec == RIGHT else LEFT
        elif d[y][x] == "7":  # right -> down, up -> left
            vec = DOWN if vec == RIGHT else LEFT
        elif d[y][x] == "F":  # left -> down, up -> right
            vec = DOWN if vec == LEFT else RIGHT

        ispipe[y][x] = True
        x += vec[0]
        y += vec[1]
        dist += 1
    return dist / 2, ispipe


def do_line(col: list[str], y: int, ispipe: list[list[bool]]):
    io = "O"
    last_bend = None
    for x, c in enumerate(col):
        if not ispipe[y][x]:
            col[x] = io
        elif c == "|":
            io = "O" if io == "I" else "I"
        elif not last_bend:
            last_bend = c
        elif c in "FJL7":
            double = last_bend + c
            if double == "FJ" or double == "L7":
                io = "O" if io == "I" else "I"
            elif double == "F7" or double == "LJ":
                pass  # Stay on same side
            last_bend = None


def prob_2(data: list[str]):
    _, ispipe = prob_1(data)

    d = [[c for c in line] for line in data]

    y = next(y for y, line in enumerate(d) if "S" in line)
    x = d[y].index("S")

    if d[y][x - 1] in "-FL":
        if d[y][x + 1] in "-7J":
            d[y][x] = "-"
        elif d[y - 1][x] in "|7F":
            d[y][x] = "J"
        elif d[y + 1][x] in "|JL":
            d[y][x] = "7"
    elif d[y][x + 1] in "-7J":
        if d[y - 1][x] in "|7F":
            d[y][x] = "L"
        elif d[y + 1][x] in "|JL":
            d[y][x] = "F"
    else:
        d[y][x] = "|"

    for y, col in enumerate(d):
        do_line(col, y, ispipe)

    return sum(sum(1 if c == "I" else 0 for c in line) for line in d)


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
