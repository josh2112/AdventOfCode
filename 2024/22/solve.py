"""https://adventofcode.com/2024/day/22"""

import argparse
import time
from collections import defaultdict

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def next_secret(n):
    n = mixprune(n << 6, n)
    n = mixprune(n // 32, n)
    return mixprune(n << 11, n)


def mixprune(n, sec):
    return (n ^ sec) % 16777216


def prob_1(data: list[str]) -> int:
    accum = 0
    for line in data:
        n = int(line)
        for i in range(2000):
            n = next_secret(n)
        accum += n
    return accum


def calc_best_total(data, iters):
    seq_seq_to_best_price = []

    for line in data:
        seq_to_best_price = defaultdict(lambda: 0)
        n = int(line)
        d0 = n - n // 10 * 10
        diff = []
        for i in range(iters):
            n = next_secret(n)
            d1 = n - n // 10 * 10
            diff.append(d1 - d0)
            if len(diff) >= 4:
                seq = tuple(diff[-4:])
                if seq not in seq_to_best_price:
                    seq_to_best_price[seq] = d1
            d0 = d1
        seq_seq_to_best_price.append(seq_to_best_price)

    best = 0
    for seq in set(k for d in seq_seq_to_best_price for k in d.keys()):
        t = sum(d[seq] for d in seq_seq_to_best_price)
        if t > best:
            print(f"{seq}: {t}")
            best = t
    return best


def prob_2(data: list[str]) -> int:
    return calc_best_total(data, 2000)


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2024 day 22.")
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
