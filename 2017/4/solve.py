"""https://adventofcode.com/2017/day/4"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def is_valid(phrase: str, part2: bool = False) -> bool:
    words = phrase.split()
    return len(words) == (
        len(set(tuple(sorted(w)) for w in words)) if part2 else len(set(words))
    )


def prob_1(data: list[str]) -> int:
    return sum(1 for line in data if is_valid(line))


def prob_2(data: list[str]) -> int:
    return sum(1 for line in data if is_valid(line, part2=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solves AoC 2017 day 4.")
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
