"""https://adventofcode.com/2015/day/12"""

import argparse
import time
import json

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def proc(obj, ignore=None) -> int:
    if isinstance(obj, int):
        return obj
    elif isinstance(obj, list):
        return sum(proc(item, ignore) for item in obj)
    elif isinstance(obj, dict):
        if any(v == ignore for k, v in obj.items()):
            return 0
        else:
            return sum(proc(v, ignore) for k, v in obj.items())
    elif isinstance(obj, str):
        return 0
    else:
        print(f"Don't know how to process type {type(obj)}")
        return 0


def prob_1(data: list[str]) -> int:
    doc = json.loads(data[0])
    return proc(doc)


def prob_2(data: list[str]) -> int:
    doc = json.loads(data[0])
    return proc(doc, "red")


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2015 day 12.")
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
