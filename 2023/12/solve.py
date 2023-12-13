#!/usr/bin/env python3

import time
import functools
from typing import Tuple

# https://adventofcode.com/2023/day/12

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2 (or 0 for test cases)
PART = 2

row: Tuple[str, ...] = ("",)


@functools.cache
def bfs(
    row_idx: int,
    repl_first: str,
    groups: Tuple[int, ...],
    group_cnt: int,
) -> int:
    for i in range(row_idx, len(row)):
        c = repl_first if i == row_idx and repl_first else row[i]
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


def test():
    global row
    row = tuple([r for r in ".????."])
    return bfs(0, "", (1, 1), 0)


def prob_1(data: list[str]):
    global row
    num = 0
    for line in data:
        rowtmp, groups = line.split()
        row = tuple([r for r in rowtmp])
        groups = [int(i) for i in groups.split(",")]
        bfs.cache_clear()
        num += bfs(0, "", tuple(groups), 0)
    return num


def prob_2(data: list[str]):
    for i in range(len(data)):
        row, groups = data[i].split()
        data[i] = (
            "?".join(row for _ in range(5)) + " " + ",".join(groups for _ in range(5))
        )
    return prob_1(data)


def main():
    with open(INPUT or "input.txt", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    start = time.perf_counter()
    match PART:
        case 0:
            result = test()
        case 1:
            result = prob_1(data)
        case 2:
            result = prob_2(data)
    elapsed = time.perf_counter() - start

    print(f"Problem {PART}: {result}")
    print(f"Time: {elapsed} s")


if __name__ == "__main__":
    main()
