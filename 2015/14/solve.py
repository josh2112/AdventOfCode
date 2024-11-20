"""https://adventofcode.com/2015/day/14"""

import argparse
import time
from dataclasses import dataclass

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


@dataclass
class Reindeer:
    name: str
    speed: int
    t_fly: int
    t_rest: int


def parse(data: list[str]) -> Reindeer:
    # Rudolph can fly 3 km/s for 4 seconds, but then must rest for 5 seconds.
    for line in data:
        tk = line.split()
        yield Reindeer(tk[0], int(tk[3]), int(tk[6]), int(tk[13]))


def prob_1(data: list[str]) -> int:
    deer: list[Reindeer] = list(parse(data))
    t = 2503
    best = 0
    for d in deer:
        # 0, 3, 6, 9, 12, 12, 12, 12, 12, 12, 15, 18, 21, 24, 24....
        # a = complete fly/rest cycles, rem = seconds left over
        a, rem = divmod(t, d.t_fly + d.t_rest)
        dist = a * d.speed * d.t_fly
        if rem < d.t_fly:
            dist += rem * d.speed
        else:
            dist += d.speed * d.t_fly

        if dist > best:
            best = dist

        print(f"{t}: {d.name} at {dist} km")
    return best


def prob_2(data: list[str]) -> int:
    print(data)
    return 0


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2015 day 14.")
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
