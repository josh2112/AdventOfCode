"""https://adventofcode.com/2015/day/10"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1

# CONWAY = 1.303577269034


def iterate(run: str, cnt: int):
    run = list(run)
    # print(f"0: {len(run)}")
    for n in range(cnt):
        s, char, consec = [], None, 0
        for c in run:
            if c == char:
                consec += 1
            else:
                if char:
                    s += [str(consec), char]
                char = c
                consec = 1
        if consec > 0:
            s += [str(consec), char]
        run = s
        # print(f"{n+1}: {len(run)}")

    return len(run)


def prob_1(data: list[str]) -> int:
    return iterate(data[0], 40)


def prob_2(data: list[str]) -> int:
    return iterate(data[0], 50)


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2015 day 10.")
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
