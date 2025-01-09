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


def parse(data: list[str]) -> list[Node]:
    nodes = [Node(int(v), None, None) for v in data]
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


def mix1(nodes: list[Node]):
    print_nodes(nodes[0], len(nodes))
    for n in nodes:
        if n.num == 0:
            continue
        n.prev.next, n.next.prev = n.next, n.prev
        dest = n
        if n.num > 0:
            for i in range(n.num):
                dest = dest.next
            n.prev, n.next = dest, dest.next
            dest.next.prev, dest.next = n, n
        elif n.num < 0:
            for i in range(-n.num):
                dest = dest.prev
            n.prev, n.next = dest.prev, dest
            dest.prev.next, dest.prev = n, n
        print(n.num, " ->")
        print_nodes(nodes[0], len(nodes))
    return nodes


def mix2(nodes: list[Node]):
    print_nodes(nodes[0], len(nodes))
    for n in nodes:
        if n.num == 0:
            continue
        d = (n.num % len(nodes)) - (1 if n.num < 0 else 0)
        if d == 0:
            if n.num < 0:
                print(n.num, "(0) ->")
                print_nodes(nodes[0], len(nodes))
                continue
            else:
                d += 1
        if d < 0:
            d += len(nodes) + 1
        print(f"{n.num} results in {d}")
        n.prev.next, n.next.prev = n.next, n.prev
        dest = n
        for i in range(d):
            dest = dest.next
        n.prev, n.next = dest, dest.next
        dest.next.prev, dest.next = n, n
        print(n.num, " ->")
        print_nodes(nodes[0], len(nodes))
    return nodes


def coords(nodes: list[Node]) -> int:
    node = next(n for n in nodes if n.num == 0)
    values = []
    for j in range(3):
        for i in range(1000):
            node = node.next
        values.append(node.num)
    return sum(values)


def prob_1(data: list[str]) -> int:
    return coords(mix2(parse(data)))


def prob_2(data: list[str]) -> int:
    nodes = parse(data)
    for n in nodes:
        n.num *= 811589153

    # for i in range(10):
    mix1(nodes)
    node = next(n for n in nodes if n.num == 0)
    values = []
    for j in range(3):
        for i in range(1000):
            node = node.next
        values.append(node.num)
    return sum(values)


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
