"""https://adventofcode.com/2015/day/19"""

import argparse
import time
from sys import maxsize

# Input file path (default is "input.txt")
INPUT = "input.ex3.txt"

# Part to solve, 1 or 2
PART = 2


def find_all(s: str, sub: str) -> list[int]:
    for i in range(len(s)):
        if s[i : i + len(sub)] == sub:
            yield i


def prob_1(data: list[str]) -> int:
    mol, repl = data[-1], [line.split(" => ") for line in data[:-2]]
    mols = set()
    for r in repl:
        for i in find_all(mol, r[0]):
            mols.add(mol[:i] + r[1] + mol[i + len(r[0]) :])

    return len(mols)


def prob_2(data: list[str]) -> int:
    mol, repl = data[-1], [line.split(" => ") for line in data[:-2]]

    # Work backwards from molecule to "e", doing the longest available substitution each time. This may not work
    # for all inputs but it does for mine...

    steps = 0
    repl = sorted(repl, key=lambda r: len(r[1]), reverse=True)
    while mol != "e":
        sub_found = False
        for r in repl:
            for i in reversed(list(find_all(mol, r[1]))):
                sub_found = True
                steps += 1
                mol = mol[:i] + r[0] + mol[i + len(r[1]) :]
        if not sub_found:
            break

    return steps if mol == "e" else -1


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2015 day 19.")
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
