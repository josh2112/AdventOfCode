"""https://adventofcode.com/2017/day/1"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def captcha(data: list[str], offset: int = 1) -> int:
    """compares every number in the list to the number 'offset' away, sums the ones that match"""
    lst = list(map(int, data))
    w = len(lst)
    return sum(lst[i] for i in range(w) if lst[(i + offset) % w] == lst[i])


def prob_1(data: list[str]) -> int:
    return captcha(data[0], 1)


def prob_2(data: list[str]) -> int:
    return captcha(data[0], len(data[0]) >> 1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solves AoC 2017 day 1.")
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
