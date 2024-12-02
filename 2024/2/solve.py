"""https://adventofcode.com/2024/day/2"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def is_safe(values: list[int]) -> bool:
    delta = [a - b for a, b in zip(values, values[1:])]
    return all(v > -4 and v < 0 for v in delta) or all(v < 4 and v > 0 for v in delta)


def is_safe_dampened(values: list[int], dampened: bool = False) -> bool:
    if is_safe(values):
        return True
    for i in range(len(values)):
        v = values[:i] + values[i + 1 :]
        delta = [a - b for a, b in zip(v, v[1:])]
        if all(v > -4 and v < 0 for v in delta) or all(v < 4 and v > 0 for v in delta):
            return True
    return False


def prob_1(data: list[str]) -> int:
    return len([1 for line in data if is_safe([int(v) for v in line.split()])])


def prob_2(data: list[str]) -> int:
    return len([1 for line in data if is_safe_dampened([int(v) for v in line.split()])])


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2024 day 2.")
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
