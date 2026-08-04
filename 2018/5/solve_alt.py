"""https://adventofcode.com/2018/day/5"""

from dataclasses import dataclass

from aoclib.runner import solve

# Input file path (or pass with -i <path>)
INPUT = "input.txt"

# Part to solve, 1 or 2 (or pass with -p <1|2|all>)
PART = 1


@dataclass
class Node:
    i: int
    prv: Node | None = None
    nxt: Node | None = None


def react(polymer: str):
    nodes: list[Node] = []
    for c in polymer:
        n = Node(ord(c))
        if nodes:
            n.prv = nodes[-1]
            nodes[-1].nxt = n

    n = nodes[0]

    while n.nxt:
        if abs(n.i - n.nxt.i) == 32:
            if n.prv:
                n.prv.nxt = n.nxt.nxt
            if n.nxt.nxt:
                n.nxt.nxt.prv = n.prv
            if n.prv:
                n = n.prv
        else:
            n = n.nxt
    while n.prv:
        n = n.prv
    cnt = 1
    while n.nxt:
        cnt += 1
        n = n.nxt
    return cnt


def prob_1(data: list[str]) -> int:
    return react(data[0])


def prob_2(data: list[str]) -> int:
    min_len = len(data[0])
    for i in range(ord("a"), ord("z") + 1):
        polymer = [c for c in data[0] if ord(c) not in (i, i - 32)]
        length = react(polymer)
        print(f"{chr(i)}: count={len(data[0]) - len(polymer)}, length={length}")
        min_len = min(min_len, length)
    return min_len


if __name__ == "__main__":
    solve(__file__, PART, INPUT, prob_1, prob_2)
