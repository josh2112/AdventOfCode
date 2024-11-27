"""https://adventofcode.com/2016/day/6"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def find_common(data: list[str], do_min: bool = False) -> str:
    msg = []
    for c in range(len(data[0])):
        hist = {}
        for r in range(len(data)):
            for ltr in data[r][c]:
                hist[ltr] = hist.get(ltr, 0) + 1
        msg.append(max(hist.items(), key=lambda kv: kv[1] * (-1 if do_min else 1))[0])
    return "".join(msg)


def prob_1(data: list[str]) -> str:
    return find_common(data)


def prob_2(data: list[str]) -> int:
    return find_common(data, True)


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2016 day 6.")
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
