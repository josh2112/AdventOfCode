"""https://adventofcode.com/2024/day/7"""

import argparse
import time
import itertools
import functools

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def solve(v: tuple[int, ...], opcombo: list[str]):
    return functools.reduce(
        lambda r, v: r + v[1]
        if v[0] == "+"
        else (r * v[1] if v[0] == "*" else int(f"{r}{v[1]}")),
        zip(opcombo, v[1:]),
        v[0],
    )


def prob_1(data: list[str]) -> int:
    accum = 0
    for eq in [tuple(map(int, line.replace(":", "").split())) for line in data]:
        r, v = eq[0], eq[1:]
        if any(
            r == solve(v, opcombo)
            for opcombo in itertools.product("+*", repeat=len(v) - 1)
        ):
            accum += r
    return accum


def prob_2(data: list[str]) -> int:
    accum = 0
    i = 1
    for eq in [tuple(map(int, line.replace(":", "").split())) for line in data]:
        print(i)
        r, v = eq[0], eq[1:]
        if any(
            r == solve(v, opcombo)
            for opcombo in itertools.product("+*|", repeat=len(v) - 1)
        ):
            accum += r
        i += 1
    return accum


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2024 day 7.")
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
