"""https://adventofcode.com/2017/day/9"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def process(data: str, part2: bool = False):
    score = 0
    cancel_next = False
    in_garbage = False
    group_lvl = 0
    garb_cnt = 0

    for c in data:
        if in_garbage:
            if cancel_next:
                cancel_next = False
            elif c == "!":
                cancel_next = True
            elif c == ">":
                in_garbage = False
            else:
                garb_cnt += 1
        elif c == "<":
            in_garbage = True
        elif c == "{":
            group_lvl += 1
        elif c == "}":
            score += group_lvl
            group_lvl -= 1

    return garb_cnt if part2 else score


def prob_1(data: list[str]) -> int:
    return process(data[0])


def prob_2(data: list[str]) -> int:
    return process(data[0], part2=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solves AoC 2017 day 9.")
    parser.add_argument("-p", "--part", choices=("1", "2", "all"), default=str(PART))
    parser.add_argument("-i", "--input", default=INPUT)
    args = parser.parse_args()

    with open(args.input, mode="r", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    start = time.perf_counter()
    if args.part in ("1", "all"):
        print(f"Part 1: {prob_1(data)}")
    if args.part in ("2", "all"):
        print(f"Part 2: {prob_2(data)}")

    print(f"Time: {time.perf_counter() - start} s")
