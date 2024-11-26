"""https://adventofcode.com/2015/day/25"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def parse(data: list[str]) -> tuple[int, int]:
    tk = data[0].split()
    return int(tk[-3][:-1]), int(tk[-1][:-1])


def next_code(code: int) -> int:
    """Can this be optimized? Can't use bitshift because very few of these will be powers of 2, can't use
    memoization because there aren't that many repeating values, divmod seems to be slower than %, pow(x,1,mod) is
    also not quite as fast"""
    return (code * 252533) % 33554393


def rc_to_idx(r: int, c: int) -> int:
    # 1) Find the index of r,1: sum(range(r))+1 = i
    # 2) Find the index of r,c: i + sum(range(2+r-1,c+r))
    return sum(range(r)) + 1 + sum(range(2 + r - 1, c + r))


def prob_1(data: list[str]) -> int:
    r, c = parse(data)

    code = 20151125
    for i in range(2, rc_to_idx(r, c) + 1):
        code = next_code(code)
    return code


def prob_2(data: list[str]) -> int:
    return "freebie!"


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2015 day 25.")
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
