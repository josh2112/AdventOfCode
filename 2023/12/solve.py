"""https://adventofcode.com/2023/day/12"""

import argparse
import time
import functools
from typing import Tuple

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2 (or 0 for test cases)
PART = 2

ROW: Tuple[str, ...] = ("",)


@functools.cache
def bfs(
    row_idx: int,
    repl_first: str,
    groups: Tuple[int, ...],
    group_cnt: int,
) -> int:
    for i in range(row_idx, len(ROW)):
        c = repl_first if i == row_idx and repl_first else ROW[i]
        if c == "#":
            # Are we out of groups or have we overrun the current group?
            if not groups or group_cnt == groups[0]:
                return 0
            group_cnt += 1
        elif c == ".":
            if group_cnt > 0:  # Are we coming off a group?
                if group_cnt != groups[0]:  # Were there not enough #s in this group?
                    return 0
                group_cnt = 0
                groups = groups[1:]
        else:  # It's a '?'
            total = 0
            if groups and group_cnt < groups[0]:
                total += bfs(i, "#", groups, group_cnt)
            if not groups or group_cnt == 0 or group_cnt == groups[0]:
                total += bfs(i, ".", groups, group_cnt)
            return total

    return 1 if not groups or (len(groups) == 1 and group_cnt == groups[0]) else 0


def prob_1(data: list[str]):
    global ROW
    num = 0
    for line in data:
        rowtmp, groups = line.split()
        ROW = tuple(rowtmp)
        groups = [int(i) for i in groups.split(",")]
        bfs.cache_clear()
        num += bfs(0, "", tuple(groups), 0)
    return num


def prob_2(data: list[str]):
    for i, r in enumerate(data):
        row, groups = r.split()
        data[i] = (
            "?".join(row for _ in range(5)) + " " + ",".join(groups for _ in range(5))
        )
    return prob_1(data)


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2023 day 12.")
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
