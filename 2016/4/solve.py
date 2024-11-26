"""https://adventofcode.com/2016/day/4"""

import argparse
import re
import time
from string import ascii_lowercase

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def prob_1(data: str) -> int:
    rsum = 0
    for r in re.findall(r"([a-z-]+)-(\d+)\[([a-z]+)\]", data):
        hist = {}
        for c in r[0]:
            if c != "-":
                hist[c] = hist.get(c, 0) + 1
        rsum += (
            int(r[1])
            if r[2]
            == "".join(
                [kv[0] for kv in sorted(hist.items(), key=lambda kv: (-kv[1], kv[0]))][
                    :5
                ]
            )
            else 0
        )

    return rsum


def prob_2(data: str) -> int:
    for r in re.findall(r"([a-z-]+)-(\d+)\[([a-z]+)\]", data):
        a = ord("a")
        nrot = int(r[1])
        name = "".join(
            ascii_lowercase[((ord(c) - a) + nrot) % len(ascii_lowercase)]
            if c != "-"
            else " "
            for c in r[0]
        )
        if "north" in name:
            return r[1]


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2016 day 4.")
    parser.add_argument("-p", "--part", choices=("1", "2", "all"), default=str(PART))
    parser.add_argument("-i", "--input", default=INPUT)
    args = parser.parse_args()
    part, infile = args.part, args.input

    with open(infile, mode="r", encoding="utf-8") as f:
        data = f.read()

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
