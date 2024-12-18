"""https://adventofcode.com/2024/day/18"""

import argparse
import heapq
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1

DIRS = ((1, 0), (0, 1), (-1, 0), (0, -1))


def solve(walls, size, start, end):
    c0, p0 = 0, (0, 0)
    q = [(c0, p0)]  # cost, pos
    visited = {p0: c0}  # pos: cost

    while q:
        c0, p0 = heapq.heappop(q)
        if p0 == end:
            return c0

        c1 = c0 + 1
        for p1 in [(p0[0] + d[0], p0[1] + d[1]) for d in DIRS]:
            if (
                0 <= p1[0] < size[0]
                and 0 <= p1[1] < size[1]
                and p1 not in walls
                and (p1 not in visited or c1 < visited[p1])
            ):
                visited[p1] = c1
                heapq.heappush(q, (c1, p1))

    return 0


def prob_1(data: list[str], filename: str) -> int:
    size = (71, 71) if filename == "input.txt" else (7, 7)
    num_bytes = 1024 if filename == "input.txt" else 12
    walls = [tuple(int(v) for v in line.split(",")) for line in data][:num_bytes]

    return solve(walls, size, (0, 0), (size[0] - 1, size[1] - 1))


def prob_2(data: list[str], filename: str) -> int:
    size = (71, 71) if filename == "input.txt" else (7, 7)
    walls = [tuple(int(v) for v in line.split(",")) for line in data]
    start, end = (0, 0), (size[0] - 1, size[1] - 1)

    for i in range(len(walls), -1, -1):
        if solve(walls[:i], size, start, end):
            return f"{walls[i][0]},{walls[i][1]}"


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2024 day 18.")
    parser.add_argument("-p", "--part", choices=("1", "2", "all"), default=str(PART))
    parser.add_argument("-i", "--input", default=INPUT)
    args = parser.parse_args()
    part, infile = args.part, args.input

    with open(infile, mode="r", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    start = time.perf_counter()
    if part in ("1", "all"):
        print(f"Part 1: {prob_1(data, infile)}")
    if part in ("2", "all"):
        print(f"Part 2: {prob_2(data, infile )}")

    elapsed = time.perf_counter() - start
    print(f"Time: {elapsed} s")

    return elapsed


if __name__ == "__main__":
    main()
