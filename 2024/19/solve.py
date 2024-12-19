"""https://adventofcode.com/2024/day/19"""

import argparse
import heapq
import time
from itertools import repeat
from multiprocessing import Pool

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 2


def is_possible(towels: list[str], pattern: str) -> bool:
    q = [0]
    length = len(pattern)

    # print(f"Evaluating {pattern}:")

    # Remove towels that can't appear in the pattern?
    origlen = len(towels)
    towels = [t for t in towels if t in pattern]
    # print(f" - Eliminated {origlen-len(towels)} of {origlen} towels")

    while q:
        n0 = heapq.heappop(q)
        if n0 == -length:
            print("Yes")
            return True

        rem = pattern[-n0:]
        # lenrem = len(rem)

        for t in towels:
            lent = len(t)
            if rem[:lent] == t:
                heapq.heappush(q, n0 - lent)
        if len(q) > 30:
            print("(too complex)")
            return False

    print("no")
    return False


def prob_1(data: list[str]) -> int:
    towels, patterns = data[0].split(", "), data[2:]

    towels.sort(key=lambda p: len(p))
    towels = set(towels).difference(
        towels[i] for i in range(len(towels)) if is_possible(towels[:i], towels[i])
    )

    towels = sorted(towels, key=lambda p: -len(p))

    return sum(1 if is_possible(towels, p) else 0 for p in patterns)


def prob_2(data: list[str]) -> int:
    towels, patterns = data[0].split(", "), data[2:]
    towels = sorted(towels, key=lambda p: -len(p))

    # Pool().starmap(is_possible, zip(repeat(towels, len(patterns)), patterns))

    return sum(1 if is_possible(towels, p) else 0 for p in patterns)


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2024 day 19.")
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
