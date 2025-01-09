"""https://adventofcode.com/2022/day/20"""

import argparse
import time
from dataclasses import dataclass

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


@dataclass
class Node:
    num: int
    prev: "Node"
    next: "Node"


def parse(data: list[str], factor: int = 1) -> list[Node]:
    nodes = [Node(int(v) * factor, None, None) for v in data]
    for i in range(len(nodes)):
        nodes[i].prev = nodes[(i - 1) % len(nodes)]
        nodes[i].next = nodes[(i + 1) % len(nodes)]
    return nodes


def print_nodes(node: Node, cnt: int):
    p = node
    for i in range(cnt):
        print(p.num, end=" ")
        p = p.next
    print()


def mix(nodes: list[Node], rounds: int = 1):
    length = len(nodes) - 1
    for r in range(rounds):
        for n in nodes:
            d = n.num % length
            if d == 0:
                continue
            n.prev.next, n.next.prev = n.next, n.prev
            dest = n
            for i in range(d):
                dest = dest.next
            n.prev, n.next = dest, dest.next
            dest.next.prev, dest.next = n, n
    return nodes


def coords(nodes: list[Node]) -> int:
    result, node = 0, next(n for n in nodes if n.num == 0)
    for j in range(3):
        for i in range(1000):
            node = node.next
        result += node.num
    return result


def prob_1(data: list[str]) -> int:
    return coords(mix(parse(data)))


def prob_2(data: list[str]) -> int:
    return coords(mix(parse(data, 811589153), 10))


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2022 day 20.")
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
