"""https://adventofcode.com/2016/day/20"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def parse(data: list[str]):
    for line in data:
        a, b = line.split("-")
        yield range(int(a), int(b) + 1)


def collapse(ranges: list[range]):
    """Joins all continguous ranges into super-ranges. Depends on the list being sorted."""
    i = 0
    while i < len(ranges) - 1:
        a, b = ranges[i], ranges[i + 1]
        newrange = range(a.start, max(a.stop, b.stop)) if b.start <= a.stop else None
        if newrange:
            ranges[i] = newrange
            del ranges[i + 1]
        else:
            i += 1
    return ranges


def prob_1(data: list[str]) -> int:
    """Returns the number after the first range (which is the lowest not in a range; if it were,
    it would have been joined with the next range)"""
    return collapse(sorted(parse(data), key=lambda r: r.start))[0].stop


def prob_2(data: list[str]) -> int:
    """Sums the empty space between each pair of ranges"""
    ranges = collapse(sorted(parse(data), key=lambda r: r.start))
    return sum(pr[1].start - pr[0].stop for pr in zip(ranges, ranges[1:]))


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2016 day 20.")
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
