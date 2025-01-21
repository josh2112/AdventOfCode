"""https://adventofcode.com/2017/day/6"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def mancala(data: list[str], part2: bool = False) -> int:
    banks = list(map(int, data[0].split()))
    hashes = {tuple(banks): 0}
    cycles = 0
    while True:
        n = max(banks)
        idx = banks.index(n)
        banks[idx] = 0
        for i in range(idx + 1, idx + 1 + n):
            banks[i % len(banks)] += 1
        cycles += 1
        if (h := tuple(banks)) in hashes:
            return cycles - hashes[h] if part2 else cycles
        hashes[h] = cycles

    return banks


def prob_1(data: list[str]) -> int:
    return mancala(data)


def prob_2(data: list[str]) -> int:
    return mancala(data, part2=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solves AoC 2017 day 6.")
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
