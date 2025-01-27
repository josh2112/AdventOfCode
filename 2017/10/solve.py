"""https://adventofcode.com/2017/day/10"""

import argparse
import logging
import time
from dataclasses import dataclass
from functools import reduce
from operator import xor

logging.basicConfig(filename="log.txt", level=logging.INFO)
logger = logging.getLogger()

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


@dataclass
class Node:
    value: int
    next: "Node"

    def list(self: "Node", count: int):
        lst, n = [self], self
        for i in range(count - 1):
            lst.append(n := n.next)
        return lst


def knot(size: int, lengths: list[int], rounds: int = 1):
    def advance(n: Node, count: int):
        for i in range(count):
            n = n.next
        return n

    nodes = [Node(i, None) for i in range(size)]

    for i in range(len(nodes)):
        nodes[i].next = nodes[(i + 1) % len(nodes)]

    head, cur = nodes[0], nodes[0]
    skip = 0

    for rounds in range(rounds):
        for ln in lengths:
            if ln < 2:
                # No list to reverse, just advance cur
                cur = advance(cur, skip + ln)
                skip += 1
                continue

            sublist = cur.list(ln)

            # Identify and detach the nodes on either side of it
            n0, n1 = next(n for n in nodes if n.next == sublist[0]), sublist[-1].next
            n0.next = sublist[-1].next = None

            # Reverse the list
            for i in range(len(sublist) - 1):
                sublist[i + 1].next = sublist[i]

            # Reattach the sublist to the sequence
            n0.next, sublist[0].next = sublist[-1], n1

            # If the head was in the list, put it back in its non-reversed position
            if head in sublist:
                head = sublist[-sublist.index(head) - 1]

            cur = advance(n1, skip)
            skip += 1

    return head


def prob_1(data: list[str]) -> int:
    head = knot(256, list(map(int, data[0].split(","))))
    return head.value * head.next.value


# Run the knot hash with day 10 part 2 specs for size, length and rounds. This will be important for day 17!
def general_knot_hash(lengths: list[int]) -> list[int]:
    head = knot(256, lengths + [17, 31, 73, 47, 23], rounds=64)
    lst = [n.value for n in head.list(256)]
    return [reduce(xor, lst[i : i + 16]) for i in range(0, 256, 16)]


def prob_2(data: list[str]) -> int:
    return "".join(f"{h:02x}" for h in general_knot_hash([ord(c) for c in data[0]]))


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
