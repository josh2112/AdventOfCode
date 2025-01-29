"""https://adventofcode.com/2017/day/16"""

import argparse
import string
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def dance(count: int, data: list[str], rounds: int = 1):
    line = list(string.ascii_lowercase[:count])

    # Repeats every 63 rounds
    for r in range(rounds % 63):
        for instr in data[0].split(","):
            if instr[0] == "s":
                n = int(instr[1:])
                line = line[-n:] + line[: len(line) - n]
            else:
                a, b = instr[1:].split("/")
                if instr[0] == "x":
                    a, b = int(a), int(b)
                else:
                    a, b = line.index(a), line.index(b)
                line[a], line[b] = line[b], line[a]

    return "".join(line)


def prob_1(data: list[str]) -> int:
    return dance(16, data)


def prob_2(data: list[str]) -> int:
    return dance(16, data, rounds=1_000_000_000)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solves AoC 2017 day 16.")
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
