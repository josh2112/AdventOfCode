"""https://adventofcode.com/2016/day/13"""

import argparse
import math
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def expand_maze(seed: int, length: int) -> list[list[bool]]:
    print(f"{length}x{length} maze")
    is_open = (
        [[False] * (length + 2)]
        + [([False] + [True] * length + [False]) for i in range(length)]
        + [[False] * (length + 2)]
    )
    x_parts = [x * x + 3 * x for x in range(length)]
    y_parts = [y + y * y for y in range(length)]
    for y in range(1, length + 1):
        for x in range(1, length + 1):
            if (
                sum(
                    1 if n == "1" else 0
                    for n in bin(
                        x_parts[x - 1] + 2 * (x - 1) * (y - 1) + y_parts[y - 1] + seed
                    )
                )
                % 2
            ):
                is_open[y][x] = False
    # for row in is_open:
    #    print("".join("." if x else "#" for x in row))
    return is_open


def find_shortest_path(
    is_open: list[list[bool]], start: tuple[int, int], target: tuple[int, int]
) -> int:
    print(f"{start} -> {target}")

    best_cost = {}  # (x,y) => cost
    q = [(0, start)]

    while q:
        cost, pos = q.pop(0)
        if pos == target:
            return cost
        for d in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            newpos, newcost = (pos[0] + d[0], pos[1] + d[1]), cost + 1
            if not is_open[newpos[1]][newpos[0]]:
                continue
            if newpos in best_cost and best_cost[newpos] <= newcost:
                continue
            best_cost[newpos] = newcost
            q.append((newcost, newpos))
    return 0


def free_space_count(
    is_open: list[list[bool]], start: tuple[int, int], limit: int
) -> int:
    best_cost = {}  # (x,y) => cost
    visited = set()
    q = [(0, start)]

    while q:
        cost, pos = q.pop(0)
        if cost > limit:
            return len(visited)
        visited.add(pos)
        for d in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            newpos, newcost = (pos[0] + d[0], pos[1] + d[1]), cost + 1
            if not is_open[newpos[1]][newpos[0]]:
                continue
            if newpos in best_cost and best_cost[newpos] <= newcost:
                continue
            best_cost[newpos] = newcost
            q.append((newcost, newpos))
    return 0


def prob_1(data: list[str], target: tuple[int, int]) -> int:
    return find_shortest_path(
        expand_maze(int(data[0]), math.ceil(max(target) / 100) * 100),
        (2, 2),
        (target[0] + 1, target[1] + 1),
    )


def prob_2(data: list[str], target: tuple[int, int]) -> int:
    return free_space_count(
        expand_maze(int(data[0]), math.ceil(max(target) / 100) * 100), (2, 2), 50
    )


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2016 day 13.")
    parser.add_argument("-p", "--part", choices=("1", "2", "all"), default=str(PART))
    parser.add_argument("-i", "--input", default=INPUT)
    args = parser.parse_args()
    part, infile = args.part, args.input

    with open(infile, mode="r", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    target = (7, 4) if infile.endswith("input.ex.txt") else (31, 39)

    start = time.perf_counter()
    if part in ("1", "all"):
        print(f"Part 1: {prob_1(data, target)}")
    if part in ("2", "all"):
        print(f"Part 2: {prob_2(data, target)}")

    elapsed = time.perf_counter() - start
    print(f"Time: {elapsed} s")

    return elapsed


if __name__ == "__main__":
    main()
