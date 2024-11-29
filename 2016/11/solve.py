"""https://adventofcode.com/2016/day/11"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def print_floors(floors):
    i = 4
    for f in reversed(floors):
        print(
            f"F{i} "
            + " ".join([g + "G" for g in f[0]])
            + " ".join([m + "M" for m in f[1]])
        )
        i -= 1


def parse(data: list[str]):
    floors = []
    for line in data:
        tk = line.replace(",", "").replace(".", "").split()
        generators = [tk[i - 1][:2] for i, t in enumerate(tk) if t == "generator"]
        microchips = [
            tk[i - 1].split("-")[0][:2] for i, t in enumerate(tk) if t == "microchip"
        ]
        floors.append((generators, microchips))
    print_floors(floors)


# Objective: Get everything to the fourth floor
# Rules: only 2 things can be in an elevator at a time
def prob_1(data: list[str]) -> int:
    floors = parse(data)
    e = 0
    return 0


def prob_2(data: list[str]) -> int:
    print(data)
    return 0


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2016 day 11.")
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
