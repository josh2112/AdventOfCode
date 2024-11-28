"""https://adventofcode.com/2016/day/9"""

import argparse
import time
import re

# Input file path (default is "input.txt")
INPUT = "input.ex2.txt"

# Part to solve, 1 or 2
PART = 2


def unzip(data: str, recurse: bool = False) -> int:
    i, count = 0, 0

    while i < len(data):
        if m := re.search(r"\((\d+)x(\d+)\)", data[i:]):
            char_cnt, rpt_cnt = int(m[1]), int(m[2])
            span = m.span(0)
            count += span[0]
            if not recurse:
                count += char_cnt * rpt_cnt
            else:
                count += (
                    unzip(data[i + span[1] : i + span[1] + char_cnt], recurse) * rpt_cnt
                )
            i += span[1] + char_cnt
        else:
            count += len(data) - i
            break
    return count


def prob_1(data: list[str]) -> int:
    return sum(unzip(line) for line in data)


def prob_2(data: list[str]) -> int:
    sums = [unzip(line, True) for line in data]
    return sum(sums)


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2016 day 9.")
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
