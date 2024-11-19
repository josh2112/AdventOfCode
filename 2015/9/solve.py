"""https://adventofcode.com/2015/day/9"""

import argparse
import time
from dataclasses import dataclass

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


@dataclass
class Edge:
    v1: str
    v2: str
    dist: int


def parse(data: list[str]) -> list[Edge]:
    for line in data:
        tk = line.split()
        yield Edge(tk[0][:2], tk[2][:2], int(tk[4]))


def prob_1(data: list[str]) -> int:
    edges_by_dist = sorted(parse(data), key=lambda e: e.dist)
    all_vertices = set(v for pr in [(e.v1, e.v2) for e in edges_by_dist] for v in pr)
    edges = []
    while True:
        e = edges_by_dist.pop(0)
        print(f"Adding {e}")
        edges.append(e)

        reachable = set(v for pr in [(e.v1, e.v2) for e in edges] for v in pr)
        print(f"still not reachable: {all_vertices.difference(reachable )}")
        if reachable == all_vertices:
            break
    print(edges)
    return sum(e.dist for e in edges)


def prob_2(data: list[str]) -> int:
    print(data)
    return 0


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2015 day 9.")
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
