"""https://adventofcode.com/2016/day/12"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def run(data: list[str], reg: dict[str, int], ic: int) -> int:
    prog = [(line + " .").split() for line in data]

    while ic < len(prog):
        instr, x, y, *_ = prog[ic]
        if instr[0] == "c":
            reg[y] = reg[x] if x in reg else int(x)
        elif instr[2] == "c":
            reg[x] += 1 * (1 if instr[0] == "i" else -1)

        if instr[0] == "j" and (reg[x] if x in reg else int(x)) != 0:
            ic += int(y)
        else:
            ic += 1

    return reg["a"]


def prob_1(data: list[str]) -> int:
    return run(data, {"a": 0, "b": 0, "c": 0, "d": 0}, 0)


def prob_2(data: list[str]) -> int:
    return run(data, {"a": 0, "b": 0, "c": 1, "d": 0}, 0)


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2016 day 12.")
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
