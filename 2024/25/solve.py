"""https://adventofcode.com/2024/day/25"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def prob_1(data: list[str]) -> int:
    locks, keys = [], []
    for i in range(0, len(data), 8):
        grid = list(zip(*data[i : i + 7]))
        if data[i] == "#####":
            locks.append(
                list(max(i for i, v in enumerate(line) if v == "#") for line in grid)
            )
        else:
            keys.append(list(len(grid) - line.index("#") + 1 for line in grid))

    return len(
        [
            1
            for lock in locks
            for key in keys
            if all(a + b <= 5 for a, b in zip(lock, key))
        ]
    )


def prob_2(data: list[str]) -> int:
    print(data)
    return 0


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2024 day 25.")
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
