"""https://adventofcode.com/2015/day/20"""

import argparse
import time

import matplotlib.pyplot as plot

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


# Find highly-composite numbers (antiprimes) and sum their factors until we get to 3_400_000
# 27720 is the 25th highly-composite number


def prob_1(data: list[str]) -> int:
    tgt = int(data[0]) / 10  # 3_400_000

    # bounds = (27720, 27720)
    bounds = (1, 120)

    cnts = []
    h = bounds[0]
    while True:
        presents = sum(e for e in range(1, h + 1) if not (h % e))

        cnts.append((h, presents))

        if h == bounds[1]:
            plot.plot(range(1, len(cnts) + 1), cnts)
            plot.show()
            break

        if presents >= tgt:
            break

        h += 1

    top = max(cnts, key=lambda f: -f[1] / f[0])
    print(top)
    print(
        "factors",
        [e for e in range(1, top[0] + 1) if not (top[0] % e)],
    )

    return h


def prob_2(data: list[str]) -> int:
    print(data)
    return 0


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2015 day 20.")
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
