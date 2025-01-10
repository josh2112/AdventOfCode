"""https://adventofcode.com/2016/day/18"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1

TRAPS = [list(cfg) for cfg in ("^^.", ".^^", "^..", "..^")]


def generate_rows(r1: list[str], cnt: int):
    for i in range(cnt):
        r0 = r1
        r0.insert(0, ".")
        r0.insert(len(r0), ".")
        r1 = ["^" if r0[i : i + 3] in TRAPS else "." for i in range(len(r0) - 2)]
        yield r1


def count_safe(row: str, num_rows: int):
    return row.count(".") + sum(
        r.count(".") for r in generate_rows(list(row), num_rows - 1)
    )


def prob_1(data: list[str]) -> int:
    return count_safe(data[0], 40)


def prob_2(data: list[str]) -> int:
    return count_safe(data[0], 400_000)


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2016 day 18.")
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
