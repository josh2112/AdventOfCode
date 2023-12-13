#!/usr/bin/env python3

import time
import itertools

# https://adventofcode.com/2023/day/13

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 2


def find_reflection(data: list[str], prob2: bool):
    for pr in itertools.pairwise(range(len(data))):
        x0, x1 = pr
        diffs = []
        while x0 >= 0 and x1 < len(data):
            diffs.append(sum(0 if p[0] == p[1] else 1 for p in zip(data[x0], data[x1])))
            if diffs[-1] > 1:
                diffs = []
                break
            x0 -= 1
            x1 += 1
        if not prob2 and len(diffs) and sum(diffs) == 0:
            return pr[0] + 1
        if prob2 and len(diffs) and sum(diffs) == 1:
            return pr[0] + 1
    return 0


def find_reflections(data: list[str], prob2: bool):
    vert = find_reflection(data, prob2)
    horiz = find_reflection(list(map(list, zip(*data))), prob2)
    return vert * 100 + horiz


def prob_1(data: list[str]):
    seps = [-1] + [i for i, d in enumerate(data) if not d] + [len(data)]
    blocks = [data[pr[0] + 1 : pr[1]] for pr in itertools.pairwise(seps)]
    return sum(find_reflections(b, False) for b in blocks)


def prob_2(data: list[str]):
    seps = [-1] + [i for i, d in enumerate(data) if not d] + [len(data)]
    blocks = [data[pr[0] + 1 : pr[1]] for pr in itertools.pairwise(seps)]
    return sum(find_reflections(b, True) for b in blocks)


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
