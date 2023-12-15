#!/usr/bin/env python3

import time

# https://adventofcode.com/2023/day/15

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 2


def prob_1(data: list[str]):
    h = 0
    for step in "".join(data).split(","):
        v = 0
        for c in step:
            v += ord(c)
            v *= 17
            v %= 256
        h += v
    return h


def prob_2(data: list[str]):
    boxes = [[] for _ in range(256)]
    for lens in "".join(data).split(","):
        if lens[-1] == "-":
            lens += "."
        lbl, b = lens[:-2], 0
        for c in lbl:
            b += ord(c)
            b *= 17
        b %= 256
        i = next((i for i, l in enumerate(boxes[b]) if l[0] == lbl), -1)
        if lens[-2] == "-":
            if i >= 0:
                del boxes[b][i]
        elif i >= 0:
            boxes[b][i] = (lbl, lens[-1])
        else:
            boxes[b].append((lbl, lens[-1]))

        # print("---")
        # for i in [i for i, b in enumerate(boxes) if b]:
        #    print(f"{i}: {boxes[i]}")

    f = 0
    for b in range(len(boxes)):
        for l in range(len(boxes[b])):
            if boxes[b][l][1] == ".":
                pass
            f += (b + 1) * (l + 1) * int(boxes[b][l][1])
    return f


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
