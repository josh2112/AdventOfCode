"""https://adventofcode.com/2024/day/14"""

import argparse
import time
import re
from collections import Counter
import math
import os
import sys

import PIL.Image

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def parse(data: list[str]):
    return [
        [int(v) for v in m.groups()]
        for m in re.finditer(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)", "\n".join(data))
    ]


def prob_1(data: list[str], bounds: tuple[int, int]) -> int:
    robots = parse(data)
    steps = 100
    for r in robots:
        r[0] = (r[0] + r[2] * steps) % bounds[0]
        r[1] = (r[1] + r[3] * steps) % bounds[1]
    mid = bounds[0] // 2, bounds[1] // 2
    return math.prod(
        Counter(
            (r[0] // (bounds[0] / 2), r[1] // (bounds[1] / 2))
            for r in robots
            if r[0] != mid[0] and r[1] != mid[1]
        ).values()
    )


def prob_2(data: list[str], bounds: tuple[int, int]) -> int:
    robots = parse(data)
    os.makedirs("imgs", exist_ok=True)
    minvar = sys.maxsize
    for i in range(0, 50_000):
        for r in robots:
            r[0] = (r[0] + r[2]) % bounds[0]
            r[1] = (r[1] + r[3]) % bounds[1]

        xm = sum(r[0] for r in robots) / len(robots)
        ym = sum(r[1] for r in robots) / len(robots)
        var = (
            sum(pow(r[0] - xm, 2) for r in robots)
            * sum(pow(r[1] - ym, 2) for r in robots)
        ) / pow(len(robots), 2)

        if var < minvar:
            minvar = var
            print(f"{i}: {minvar}")
            img = [0] * bounds[0] * bounds[1]
            for r in robots:
                img[r[1] * bounds[0] + r[0]] = 255
            PIL.Image.frombytes(
                mode="L",
                size=bounds,
                data=bytes(img),
            ).convert("1").save(
                f"imgs/{i}.png",
            )
        elif not (i % 10_000):
            print(i)

    return 0


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2024 day 14.")
    parser.add_argument("-p", "--part", choices=("1", "2", "all"), default=str(PART))
    parser.add_argument("-i", "--input", default=INPUT)
    args = parser.parse_args()
    part, infile = args.part, args.input

    with open(infile, mode="r", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    tmp = infile.split(".")
    tmp.insert(-1, "bounds")
    with open(".".join(tmp), mode="r", encoding="utf-8") as f:
        bounds = [int(v) for v in f.readline().split(",")]

    start = time.perf_counter()
    if part in ("1", "all"):
        print(f"Part 1: {prob_1(data, bounds)}")
    if part in ("2", "all"):
        print(f"Part 2: {prob_2(data, bounds)}")

    elapsed = time.perf_counter() - start
    print(f"Time: {elapsed} s")

    return elapsed


if __name__ == "__main__":
    main()
