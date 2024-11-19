"""https://adventofcode.com/2015/day/6"""

import argparse
import time

import PIL.Image

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def prob_1(data: list[str]) -> int:
    w, h = 1000, 1000
    lights = [[False] * w for i in range(h)]

    for ln in data:
        tk = ln.split()
        c1, c2 = (
            [int(n) for n in tk[-3].split(",")],
            [int(n) for n in tk[-1].split(",")],
        )
        for x in range(c1[0], c2[0] + 1):
            for y in range(c1[1], c2[1] + 1):
                if tk[0].startswith("to"):  # toggle
                    lights[y][x] = not lights[y][x]
                elif tk[1][1] == "n":  # turn oN
                    lights[y][x] = True
                else:  # turn off
                    lights[y][x] = False

    PIL.Image.frombytes(
        mode="L",
        size=(w, h),
        data=bytes([255 if i else 0 for row in lights for i in row]),
    ).convert("1").show()

    return sum(1 if i else 0 for row in lights for i in row)


def prob_2(data: list[str]) -> int:
    w, h = 1000, 1000
    lights = [[0] * w for i in range(h)]

    for ln in data:
        tk = ln.split()
        c1, c2 = (
            [int(n) for n in tk[-3].split(",")],
            [int(n) for n in tk[-1].split(",")],
        )
        for x in range(c1[0], c2[0] + 1):
            for y in range(c1[1], c2[1] + 1):
                if tk[0].startswith("to"):  # toggle (+2)
                    lights[y][x] += 2
                elif tk[1][1] == "n":  # turn oN (+1)
                    lights[y][x] += 1
                elif lights[y][x] > 0:  # turn off (-1, min=0)
                    lights[y][x] -= 1

    PIL.Image.frombytes(
        mode="L",
        size=(w, h),
        data=bytes([i for row in lights for i in row]),
    ).show()

    return sum(i for row in lights for i in row)


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2015 day 6.")
    parser.add_argument("-p", "--part", choices=("1", "2", "all"), default=str(PART))
    parser.add_argument("-i", "--input", default=INPUT)
    args = parser.parse_args()

    with open(args.input, mode="r", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    start = time.perf_counter()
    if args.part in ("1", "all"):
        print(f"Part 1: {prob_1(data)}")
    if args.part in ("2", "all"):
        print(f"Part 2: {prob_2(data)}")

    elapsed = time.perf_counter() - start
    print(f"Time: {elapsed} s")

    return elapsed


if __name__ == "__main__":
    main()
