"""https://adventofcode.com/2022/day/16"""

import argparse
import heapq
import re
import time
from dataclasses import dataclass

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


@dataclass
class Valve:
    name: str
    rate: int
    neighbors: "list[str]"


def parse(data: list[str]):
    for line in data:
        name, rate, neighbors = re.match(
            r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? ([\w, ]*)",
            line,
        ).groups()
        yield Valve(name, int(rate), neighbors.split(", "))


def prob_1(data: list[str]) -> int:
    valves = list(parse(data))
    valves_by_name = {v.name: v for v in valves}

    c0, p0 = 0, valves_by_name["AA"]

    # minutes used, valve, total release
    q = [
        (
            c0,
            p0,
        )
    ]
    visited = {p0: c0}

    while q:
        c0, p0 = heapq.heappop(q)

    return 0


def prob_2(data: list[str]) -> int:
    print(data)
    return 0


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2022 day 16.")
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
