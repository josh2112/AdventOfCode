"""https://adventofcode.com/2023/day/5"""

import argparse
from dataclasses import dataclass, field
import time
import sys

# Input file path (default is "input.txt")
INPUT = "input.ex.txt"

# Part to solve, 1 or 2
PART = 2


@dataclass
class Range:
    src: range
    dst: range

    def __init__(self, dst: int, src: int, length: int):
        self.dst = range(dst, dst + length)
        self.src = range(src, src + length)


@dataclass
class Mapping:
    ranges: list[Range] = field(default_factory=list)

    def map(self, seed: int):
        r = next(
            (r for r in self.ranges if seed in r.src),
            None,
        )
        return seed + r.dst.start - r.src.start if r else seed

    def map_rev(self, seed: int):
        r = next(
            (r for r in self.ranges if seed in r.dst),
            None,
        )
        return seed + r.src.start - r.dst.start if r else seed


def make_mappings(data: list[str]):
    m = Mapping()
    for line in data[3:]:
        if not line:
            continue
        if line[0].isalpha():
            yield m
            m = Mapping()
        else:
            m.ranges.append(Range(*[int(v) for v in line.split()]))
    return m


def find_best_location(
    seeds: list[int],
    mappings: list[Mapping],
    prev_best: tuple[int, int] = (-1, sys.maxsize),
) -> tuple[int, int]:
    best = prev_best
    for seed in seeds:
        v = seed
        for m in mappings:
            v = m.map(v)
        if not best or v < best[1]:
            best = (seed, v)
    return best


def find_best_location_rev(seed_ranges: list[range], mappings: list[Mapping]):
    mappings = list(reversed(mappings))
    loc = 0
    while True:
        v = loc
        for m in mappings:
            v = m.map_rev(v)
        # is v a valid seed?
        if next((r 
        for r in seed_ranges if v in r), None):
            return loc
        if not loc % 1000000:
            print(loc)
        loc += 1


def prob_1(data: list[str]):
    seeds = [int(s) for s in data[0].split()[1:]]
    mappings = list(make_mappings(data))
    return find_best_location(seeds, mappings)[1]


def prob_2(data: list[str]):
    mappings = list(make_mappings(data))
    sr = [int(s) for s in data[0].split()[1:]]
    seed_ranges = [range(sr[i], sr[i] + sr[i + 1]) for i in range(0, len(sr), 2)]
    return find_best_location_rev(seed_ranges, mappings)


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2023 day 5.")
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
