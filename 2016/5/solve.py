"""https://adventofcode.com/2016/day/5"""

import argparse
import time
from hashlib import md5

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def prob_1(data: list[str]) -> int:
    i, n = 0, 0
    pwd = []
    while n < 8:
        hash = md5((data[0] + str(i)).encode())
        hx = hash.hexdigest()
        if hx[:5] == "00000":
            pwd += hx[5]
            n = len(pwd)
            print(hx[5], hx, hash.digest())
        i += 1
    return "".join(pwd)


def prob_2(data: list[str]) -> int:
    i, n = 0, 0
    pwd = [c for c in "--------"]
    while n < 8:
        hash = md5((data[0] + str(i)).encode())
        hx = hash.hexdigest()
        if (
            hx[:5] == "00000"
            and hx[5].isdigit()
            and int(hx[5]) < 8
            and pwd[int(hx[5])] == "-"
        ):
            pwd[int(hx[5])] = hx[6]
            n += 1
            print("".join(pwd))
        i += 1
    return "".join(pwd)


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2016 day 5.")
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
