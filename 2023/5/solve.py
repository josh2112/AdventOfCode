#!/usr/bin/env python3

from dataclasses import dataclass, field
import time

# https://adventofcode.com/2023/day/5

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 2


@dataclass
class Range:
    dst_start: int
    src_start: int
    length: int


@dataclass
class Mapping:
    ranges: list[Range] = field(default_factory=list)

    def map(self, seed: int):
        r = next((r for r in self.ranges if seed >= r.src_start and seed <= r.src_start + r.length), None)
        return seed + r.dst_start - r.src_start if r else seed


def find_best_location(seeds: list[int], data: list[str]):
    mappings: list[Mapping] = []
    for line in data[1:]:
        if not line:
            continue
        if line[0].isalpha():
            mappings.append(Mapping())
        else:
            mappings[-1].ranges.append(Range(*[int(v) for v in line.split()]))
    best = None
    for seed in seeds:
        v = seed
        for m in mappings:
            v = m.map(v)
        if not best or v < best[1]:
            best = (seed, v)
    return best[1]


def prob_1(data: list[str]):
    seeds = [int(s) for s in data[0].split()[1:]]
    return find_best_location(seeds, data)


def prob_2(data: list[str]):
    seed_ranges = [int(s) for s in data[0].split()[1:]]
    seeds = [list(range(seed_ranges[i], seed_ranges[i] + seed_ranges[i + 1])) for i in range(0, len(seed_ranges), 2)]
    seeds = [s for g in seeds for s in g]
    return find_best_location(seeds, data)


def main():
    with open(INPUT or "input.txt", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    start = time.perf_counter()
    result = prob_1(data) if PART == 1 else prob_2(data)
    elapsed = time.perf_counter() - start

    print(f"Problem {PART}: {result}")
    print(f"Time: {elapsed} s")


if __name__ == "__main__":
    main()
