#!/usr/bin/env python3

import more_itertools
import time
import re

# https://adventofcode.com/2023/day/12

# Input file path (default is "input.txt")
INPUT = "input.ex.txt"

# Part to solve, 1 or 2
PART = 2


def prob_1(data: list[str]):
    num = 0
    for line in data:
        print(data.index(line))
        row, groups = line.split()
        groups = [int(i) for i in groups.split(",")]
        qs = [i for i, c in enumerate(row) if c == "?"]
        needed = sum(int(i) for i in groups) - len([c for c in row if c == "#"])

        for repl in more_itertools.distinct_permutations(
            ["."] * (len(qs) - needed) + ["#"] * needed
        ):
            last = "."
            repl_index = 0
            group_cnt = 0
            group_index = 0
            fail = False
            # print("Trying", repl)
            for c in row:
                if c == "?":
                    c = repl[repl_index]
                    repl_index += 1
                if c == "." and last == "#":
                    # end of group
                    if group_cnt == groups[group_index]:
                        group_index += 1
                        group_cnt = 0
                    else:
                        fail = True
                        break
                elif c == "#":
                    group_cnt += 1
                last = c
            if not fail and (
                group_index == len(groups) or group_cnt == groups[group_index]
            ):
                num += 1
    return num


# This doesn't complete even the first line of the real input :-/
# TODO: Alternate approach - recursion? Walk the string, every time we see a '?'
# branch out into possibilities of . and #, stopping if we break a group constraint


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
    result = prob_1(data) if PART == 1 else prob_2(data)
    elapsed = time.perf_counter() - start

    print(f"Problem {PART}: {result}")
    print(f"Time: {elapsed} s")


if __name__ == "__main__":
    main()
