"""https://adventofcode.com/2024/day/23"""

import argparse
import itertools
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def prob_1(data: list[str]) -> int:
    edges = [(line[0:2], line[3:5]) for line in data]
    computers = set(c for e in edges for c in e)
    edges += [(e[1], e[0]) for e in edges]

    groups = set()
    for c in computers:
        pals = [e[1] for e in edges if e[0] == c]
        for pr in itertools.combinations(pals, 2):
            if (pr[0], pr[1]) in edges and (
                c[0] == "t" or pr[0][0] == "t" or pr[1][0] == "t"
            ):
                groups.add(tuple(sorted((c, pr[0], pr[1]))))

    print("\n".join(",".join(c for c in g) for g in groups))
    return len(groups)


def prob_2(data: list[str]) -> int:
    edges = [(line[0:2], line[3:5]) for line in data]
    computers = set(c for e in edges for c in e)
    edges += [(e[1], e[0]) for e in edges]

    conns = {}
    for c in computers:
        pals = [e[1] for e in edges if e[0] == c]
        print(c, ":", pals)

    return 0


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2024 day 23.")
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