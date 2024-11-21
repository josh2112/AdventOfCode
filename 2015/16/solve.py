"""https://adventofcode.com/2015/day/16"""

import argparse
import pprint
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 2

TARGET = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}


def parse(data: list[str]) -> dict[str, int]:
    # Sue 10: perfumes: 5, pomeranians: 4, children: 9
    for line in data:
        tk = line.split()
        yield {
            tk[2][:-1]: int(tk[3][:-1]),
            tk[4][:-1]: int(tk[5][:-1]),
            tk[6][:-1]: int(tk[7]),
        }


def prob_1(data: list[str]) -> int:
    aunts = list(parse(data))
    for i, aunt in enumerate(aunts):
        ismatch = all(k not in aunt or aunt[k] == TARGET[k] for k in TARGET)
        if ismatch:
            return i + 1


def prob_2(data: list[str]) -> int:
    aunts = list(parse(data))
    more_keys, less_keys = ("cats", "trees"), ("pomeranians", "goldfish")
    exact_keys = set(k for a in aunts for k in a.keys()).difference(
        more_keys + less_keys
    )
    for i, aunt in enumerate(aunts):
        ismatch = all(k not in aunt or aunt[k] == TARGET[k] for k in exact_keys)
        ismatch &= all(k not in aunt or aunt[k] > TARGET[k] for k in more_keys)
        ismatch &= all(k not in aunt or aunt[k] < TARGET[k] for k in less_keys)
        if ismatch:
            return i + 1


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2015 day 16.")
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
