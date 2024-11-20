"""https://adventofcode.com/2015/day/13"""

import argparse
import time
from itertools import permutations

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def calc_dist(path: tuple[str, ...], edges: dict[tuple[str, str], int]) -> int:
    return sum(edges[hop] + edges[(hop[1], hop[0])] for hop in zip(path, path[1:]))


def parse(data: list[str]) -> tuple[tuple[str, str], int]:
    # Alice would gain 54 happiness units by sitting next to Bob.
    for line in data:
        tk = line.split()
        k1, k2 = tk[0][0], tk[10][0]
        d = int(tk[3]) * (-1 if tk[2] == "lose" else 1)
        yield (k1, k2), d


def find_worst(edges) -> tuple[list[int], int]:
    worst = (None, 0)  # path, dist
    for path in permutations(set(v for pr in edges for v in pr)):
        path = list(path) + [path[0]]  # Link back to start
        dist = calc_dist(path, edges)
        if dist > worst[1]:
            worst = (path, dist)
    return worst


def prob_1(data: list[str]) -> int:
    edges = dict(parse(data))
    return find_worst(edges)


def prob_2(data: list[str]) -> int:
    edges = dict(parse(data))
    for node in set(v for pr in edges for v in pr):
        edges[(node, "J")] = 0
        edges[("J", node)] = 0
    return find_worst(edges)


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2015 day 13.")
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
