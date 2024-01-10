"""https://adventofcode.com/2023/day/15"""

import argparse
import time


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
    for b, box in enumerate(boxes):
        for l, lens in enumerate(box):
            if lens[1] == ".":
                pass
            f += (b + 1) * (l + 1) * int(lens[1])
    return f


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2023 day 15.")
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
