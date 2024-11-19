"""https://adventofcode.com/2015/day/5"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1

VOWELS = "aeiou"
DISALLOWED = ("ab", "cd", "pq", "xy")


def is_nice(data: str) -> bool:
    num_vowels = 1 if data[0] in VOWELS else 0
    num_double_letters = 0
    for pair in zip(data, data[1:]):
        if "".join(pair) in DISALLOWED:
            return False
        if pair[1] in VOWELS:
            num_vowels += 1
        if pair[0] == pair[1]:
            num_double_letters += 1
    return num_vowels >= 3 and num_double_letters >= 1


def is_nice2(data: str) -> bool:
    return any(
        data[i : i + 2] in "".join(data[0:i])
        or data[i : i + 2] in "".join(data[i + 2 :])
        for i in range(len(data) - 2)
    ) and any(data[i] == data[i + 2] for i in range(len(data) - 2))


def prob_1(data: list[str]) -> int:
    return sum(1 if is_nice(ln) else 0 for ln in data)


def prob_2(data: list[str]) -> int:
    return sum(1 if is_nice2(ln) else 0 for ln in data)


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2015 day 5.")
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
