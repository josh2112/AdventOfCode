"""https://adventofcode.com/2024/day/6"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1

DIRS = ((0, -1), (1, 0), (0, 1), (-1, 0))


def parse(data: list[str]):
    walls = []
    guard = (0, 0)
    for y, row in enumerate(data):
        for x, sq in enumerate(row):
            if sq == "#":
                walls.append((x, y))
            elif sq == "^":
                guard = (x, y)
    return walls, (len(data[0]), len(data)), guard


def printmaze(walls, size, visited):
    dchr = "^>v<"
    maze = [["."] * size[0] for i in range(size[1])]
    for w in walls:
        maze[w[1]][w[0]] = "#"
    for p, d in visited:
        maze[p[1]][p[0]] = dchr[d]
    for line in maze:
        print("".join(line))


def prob_1(data: list[str]) -> int:
    walls, size, g = parse(data)
    di = 0
    visited = set((g,))

    while True:
        nxt = (g[0] + DIRS[di][0], g[1] + DIRS[di][1])
        if nxt[0] >= size[0] or nxt[0] < 0 or nxt[1] >= size[1] or nxt[1] < 0:
            break
        if nxt in walls:
            di = (di + 1) % len(DIRS)
        else:
            g = nxt
            visited.add(nxt)

    return len(visited)


def prob_2(data: list[str]) -> int:
    walls, size, g = parse(data)
    di = 0
    visited = []

    while True:
        nxt = (g[0] + DIRS[di][0], g[1] + DIRS[di][1])
        if nxt[0] >= size[0] or nxt[0] < 0 or nxt[1] >= size[1] or nxt[1] < 0:
            break

        if nxt in walls:
            di = (di + 1) % len(DIRS)
        else:
            g = nxt
            visited.append((nxt, di))

    tmpwallpos = set()

    for i in range(len(visited) - 1, 0, -1):
        print(i)
        vold = visited[: i - 1]
        vnew = []
        tmpwall = visited[i][0]
        g, di = visited[i - 1]
        while True:
            nxt = (g[0] + DIRS[di][0], g[1] + DIRS[di][1])
            if nxt[0] >= size[0] or nxt[0] < 0 or nxt[1] >= size[1] or nxt[1] < 0:
                break

            if nxt in walls or nxt == tmpwall:
                di = (di + 1) % len(DIRS)
            else:
                g = nxt
                if (nxt, di) in vold or (nxt, di) in vnew:
                    tmpwallpos.add(tmpwall)
                    break
                vnew.append((nxt, di))

    # 1822 and 1821 are too high
    # 1715 also too high
    return len(tmpwallpos)


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2024 day 6.")
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
