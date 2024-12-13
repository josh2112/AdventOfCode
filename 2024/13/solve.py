"""https://adventofcode.com/2024/day/13"""

import argparse
import time
import re

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def parse(data: list[str]) -> int:
    return [
        [
            [int(v) for v in re.match(r".*[\+|\=](\d+).*[\+|\=](\d+)", line).groups()]
            for line in data[i : i + 3]
        ]
        for i in range(0, len(data), 4)
    ]


def solve(data: list[str], p2: bool = False) -> int:
    tokens = 0
    for m in parse(data):
        t, u, v, w, x, y = (
            m[0][0],
            m[0][1],
            m[1][0],
            m[1][1],
            m[2][0] + (10000000000000 if p2 else 0),
            m[2][1] + (10000000000000 if p2 else 0),
        )
        b = round((y - u * x / t) / (w - u * v / t))
        a = round(x / t - v * b / t)

        if (
            (p2 or a <= 100)
            and (p2 or b <= 100)
            and (t * a + v * b) == x
            and (u * a + w * b) == y
        ):
            tokens += 3 * a + b

    return tokens


def prob_1(data: list[str]) -> int:
    return solve(data)


def prob_2(data: list[str]) -> int:
    return solve(data, p2=True)


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2024 day 13.")
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
