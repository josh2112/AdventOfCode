"""https://adventofcode.com/2024/day/1"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def prob_1(data: list[str]) -> int:
    # print( [int(line.split()[0]) for line in data])
    pairs = list(tuple(map(int, line.split())) for line in data)
    print(
        sum(
            abs(pr[1] - pr[0])
            for pr in zip(sorted(p[0] for p in pairs), sorted(p[1] for p in pairs))
        )
    )
    return 0


def prob_2(data: list[str]) -> int:
    pairs = list(tuple(map(int, line.split())) for line in data)
    x, y = [p[0] for p in pairs], [p[1] for p in pairs]
    histo = {}
    for v in y:
        histo[v] = histo.get(v, 0) + 1
    return sum(v * histo.get(v, 0) for v in x)


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2024 day 1.")
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
