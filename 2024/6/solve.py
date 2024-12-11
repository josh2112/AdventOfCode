"""https://adventofcode.com/2024/day/6"""

import argparse
import pickle
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
        if not (0 <= nxt[0] < size[0] and 0 <= nxt[1] < size[1]):
            break
        if nxt in walls:
            di = (di + 1) % len(DIRS)
        else:
            g = nxt
            visited.add(g)

    return len(visited)


def find_cycle(walls, size, g, di, visited):
    # Put a wall in front of us and turn
    tmpwall = (g[0] + DIRS[di][0], g[1] + DIRS[di][1])
    if next((p for p, v in visited if p == tmpwall), None):
        # print("wall cannot be placed at", tmpwall)
        return None

    di = (di + 1) % len(DIRS)

    projvisited = [(g, di)]

    while True:
        nxt = (g[0] + DIRS[di][0], g[1] + DIRS[di][1])

        if not (0 <= nxt[0] < size[0] and 0 <= nxt[1] < size[1]):
            # Out of maze? end
            # print("wall at", tmpwall, "does not cause cycle")
            return None

        if nxt in walls or nxt == tmpwall:
            # Hit a wall? Turn
            di = (di + 1) % len(DIRS)
            # Have we hit this wall and made this turn before?
            if (g, di) in visited or (g, di) in projvisited:
                # print("wall at", tmpwall, "causes cycle at", (g, di))
                return tmpwall
        else:
            g = nxt
            if (g, di) in visited or (g, di) in projvisited:
                # print("wall at", tmpwall, "causes cycle at", (g, di))
                return tmpwall
            projvisited.append((g, di))


def prob_2(data: list[str]) -> int:
    walls, size, g = parse(data)
    di = 0
    visited = [(g, di)]

    walls_producing_cycle = set()

    while True:
        nxt = (g[0] + DIRS[di][0], g[1] + DIRS[di][1])

        if not (0 <= nxt[0] < size[0] and 0 <= nxt[1] < size[1]):
            # Out of maze? end
            break

        if nxt in walls:
            # Hit a wall? Turn and record new vector
            di = (di + 1) % len(DIRS)
        else:
            # TODO: Wall cannot be placed on an existing path? Otherwise the guard will never get to it?
            if w := find_cycle(walls, size, g, di, visited):
                walls_producing_cycle.add(w)
            g = nxt
            visited.append((g, di))

    return len(walls_producing_cycle)


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
