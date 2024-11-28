"""https://adventofcode.com/2016/day/10"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def prob_1(data: list[str]) -> int:
    bots = {}
    for line in [ln for ln in data if ln[0] == "v"]:
        tk = line.split()
        bot, value = int(tk[-1]), int(tk[1])
        print(bot, value)
        lst = bots.get(bot, [])
        lst.append(value)
        bots[bot] = lst
    for line in [ln for ln in data if ln[0] == "b"]:
        tk = line.split()
        bot, low, high = (
            int(tk[1]),
            int(tk[6]) * (-1 if tk[5][0] == "o" else 1),
            int(tk[-1]) * (-1 if tk[-2][0] == "o" else 1),
        )
        print(bot, low, high)
    # print(bots)
    return 0


def prob_2(data: list[str]) -> int:
    print(data)
    return 0


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2016 day 10.")
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
