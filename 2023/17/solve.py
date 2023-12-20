#!/usr/bin/env python3

import sys
import time

# https://adventofcode.com/2023/day/17

# Input file path (default is "input.txt")
INPUT = "input.ex2.txt"

# Part to solve, 1 or 2
PART = 1


def neighbors(nx: int, ny: int, xmax: int, ymax: int):
    if nx > 0:
        yield (nx - 1, ny)
    if nx < xmax - 1:
        yield (nx + 1, ny)
    if ny > 0:
        yield (nx, ny - 1)
    if ny < ymax - 1:
        yield (nx, ny + 1)


# TODO Getting 119 instead of 102 for example input. Pathological example input.ex2.txt looks right?
def prob_1(data: list[str]):
    xmax, ymax = len(data[0]), len(data)
    Q = [(x, y) for x in range(xmax) for y in range(ymax)]

    dist = [[sys.maxsize for _ in range(xmax)] for _ in range(ymax)]
    dist[0][0] = 0
    prev = [[(-1, -1) for _ in range(xmax)] for _ in range(ymax)]
    prev_straight_length = [[((0, 0), 0) for _ in range(xmax)] for _ in range(ymax)]

    while Q:
        u = sorted(Q, key=lambda q: dist[q[1]][q[0]])[0]
        Q.remove(u)

        for v in [n for n in neighbors(u[0], u[1], xmax, ymax) if n in Q]:
            alt = dist[u[1]][u[0]] + int(data[v[1]][v[0]])
            if alt < dist[v[1]][v[0]]:
                # First: can we go this way?
                vec = (v[0] - u[0], v[1] - u[1])
                str8 = prev_straight_length[u[1]][u[0]]
                if str8[0] == vec:
                    # If we've already moved 3 tiles in the same direction, no go
                    if str8[1] == 3:
                        continue
                    prev_straight_length[v[1]][v[0]] = (str8[0], str8[1] + 1)
                else:
                    prev_straight_length[v[1]][v[0]] = (vec, 1)

                dist[v[1]][v[0]] = alt
                prev[v[1]][v[0]] = u

    for line in dist:
        print(",".join(str(d) for d in line))
    print()

    DEST = (4, 1)

    track = [DEST]
    n = prev[DEST[1]][DEST[0]]
    while n != (0, 0):
        track.append(n)
        n = prev[n[1]][n[0]]
    track.append((0, 0))

    print(list(reversed(track)))

    print(prev_straight_length[ymax - 1][xmax - 1])


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
