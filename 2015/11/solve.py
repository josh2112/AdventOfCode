"""https://adventofcode.com/2015/day/11"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1

ORD_A = ord("a")
INVALID = [ord(c) - 97 for c in "iol"]


def inc_pwd(pwd: list[int]) -> str:
    i = len(pwd) - 1
    while True:
        pwd[i] += 1
        if pwd[i] > 25:
            pwd[i] = 0
            i -= 1
            if i < 0:
                pwd.insert(0, 0)
                break
        else:
            break
    return pwd


def has_run(pwd: list[int]) -> bool:
    dx = [pwd[i] - pwd[i - 1] for i in range(len(pwd))]
    return "11" in "".join("1" if c == 1 else "0" for c in dx)


def has_double_rpt(pwd: list[int]) -> bool:
    i = 1
    num_pairs = 0
    while i < len(pwd):
        if pwd[i] == pwd[i - 1]:
            num_pairs += 1
            i += 1
        i += 1
    return num_pairs > 1


def prob_1(data: list[str]) -> str:
    pwd = [ord(c) - ORD_A for c in data[0]]
    while True:
        pwd = inc_pwd(pwd)
        if (
            has_double_rpt(pwd)
            and has_run(pwd)
            and not any(inv in pwd for inv in INVALID)
        ):
            return "".join(chr(i + ORD_A) for i in pwd)


def prob_2(data: list[str]) -> int:
    pwd = prob_1(data)
    return prob_1([pwd])


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2015 day 11.")
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
