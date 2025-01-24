"""https://adventofcode.com/2017/day/10"""

import argparse
import time
from dataclasses import dataclass

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


@dataclass
class Node:
    value: int
    next: "Node"


def printlist(head: Node, len: int):
    c = head
    values = []
    for i in range(len):
        values.append(c.value)
        c = c.next
    print(" ".join(str(c) for c in values))


def knot(size: int, lengths: list[int]):
    nodes = [Node(i, None, None) for i in range(size)]
    for i in range(len(nodes)):
        nodes[i].next = nodes[(i + 1) % len(nodes)]
    head, cur = nodes[0], nodes[0]

    printlist(head, size)

    skip = 0
    for ln in lengths:
        sub, s = [], cur
        for i in range(ln):
            sub.append(s)
            s = s.next

        skip += 1


def prob_1(data: list[str]) -> int:
    # return knot( 256, list(map(int,data[0])))
    return knot(5, [3, 4, 1, 5])


def prob_2(data: list[str]) -> int:
    print(data)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solves AoC 2017 day 10.")
    parser.add_argument("-p", "--part", choices=("1", "2", "all"), default=str(PART))
    parser.add_argument("-i", "--input", default=INPUT)
    args = parser.parse_args()

    with open(args.input, mode="r", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    start = time.perf_counter()
    if args.part in ("1", "all"):
        print(f"Part 1: {prob_1(data)}")
    if args.part in ("2", "all"):
        print(f"Part 2: {prob_2(data)}")

    print(f"Time: {time.perf_counter() - start} s")
