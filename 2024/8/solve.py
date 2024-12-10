"""https://adventofcode.com/2024/day/8"""

import argparse
import itertools
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def count_nodes(data: list[str], do_harmonics: bool = False) -> int:
    ants: dict[str, list[tuple[int, int]]] = {}
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char != ".":
                ants.setdefault(char, []).append((x, y))
    xmax, ymax = len(data[0]), len(data)

    nodes: set[tuple[int, int]] = set()
    for k, v in ants.items():
        for pr in itertools.combinations(v, 2):
            dx, dy = pr[1][0] - pr[0][0], pr[1][1] - pr[0][1]
            m = 0 if do_harmonics else 1
            while True:
                n = (pr[0][0] - dx * m, pr[0][1] - dy * m)
                if not (0 <= n[0] < xmax and 0 <= n[1] < ymax):
                    break
                nodes.add(n)
                if not do_harmonics:
                    break
                m += 1
            m = 0 if do_harmonics else 1
            while True:
                n = (pr[1][0] + dx * m, pr[1][1] + dy * m)
                if not (0 <= n[0] < xmax and 0 <= n[1] < ymax):
                    break
                nodes.add(n)
                if not do_harmonics:
                    break
                m += 1
    return len(nodes)


def prob_1(data: list[str]) -> int:
    return count_nodes(data, False)


def prob_2(data: list[str]) -> int:
    return count_nodes(data, True)


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2024 day 8.")
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
