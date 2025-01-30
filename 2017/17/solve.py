"""https://adventofcode.com/2017/day/17"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.ex.txt"

# Part to solve, 1 or 2
PART = 2


def prob_1(data: list[str]) -> int:
    stepsize = int(data[0])
    buf, i = [0], 0

    for v in range(1, 2018):
        i = (i + stepsize + 1) % len(buf)
        buf.insert(i, v)

    return buf[(i + 1) % len(buf)]


def prob_2(data: list[str]) -> int:
    stepsize = int(data[0])
    i, iz = 1, 1
    vz = 1

    for v in range(2, 50_000_000):
        i = (i + stepsize + 1) % v
        if iz > i:
            iz += 1
        elif iz == i:
            vz = v

    return vz


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solves AoC 2017 day 17.")
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

    print(f"Time: {time.perf_counter() - start} s")
