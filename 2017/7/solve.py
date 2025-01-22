"""https://adventofcode.com/2017/day/7"""

import argparse
import re
import time
from dataclasses import dataclass

# Input file path (default is "input.txt")
INPUT = "input.ex.txt"

# Part to solve, 1 or 2
PART = 2


@dataclass
class Node:
    name: str
    weight: int
    children: "list[Node]"
    total_weight: int = 0


def parse(data: str):
    defs = [
        (n, int(w), c.split(", ") if c else [])
        for n, w, c in re.findall(r"(\w+) \((\d+)\)(?: -> )?([\w, ]+)?", data)
    ]
    nodes = {d[0]: Node(d[0], d[1], None) for d in defs}
    for d in defs:
        nodes[d[0]].children = [nodes[c] for c in d[2]]
    return nodes


def find_root(nodes: dict[str, Node]) -> Node:
    cur = next(iter(nodes.values()))
    while p := next((n for n in nodes.values() if cur in n.children), None):
        cur = p
    return cur


def calc_total_weight(node: Node):
    """Recursively fill in total_weights"""
    node.total_weight = node.weight + sum(calc_total_weight(c) for c in node.children)
    return node.total_weight


def trace_unbalanced(node: Node, parent: Node):
    """Finds the deepest node in the tree whose total_weight doesn't match its siblings"""
    sc = sorted(node.children, key=lambda c: c.total_weight)
    if sc[0].total_weight != sc[-1].total_weight:
        return trace_unbalanced(
            sc[0] if sc[1].total_weight == sc[-1].total_weight else sc[-1], node
        )
    else:
        return node, parent


def prob_1(data: str) -> int:
    return find_root(parse(data)).name


def prob_2(data: list[str]) -> int:
    nodes = parse(data)
    root = find_root(nodes)
    calc_total_weight(root)

    bad, bad_parent = trace_unbalanced(root, None)
    good_weight = next(
        c for c in bad_parent.children if c.total_weight != bad.total_weight
    ).total_weight

    return bad.weight - bad.total_weight + good_weight


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solves AoC 2017 day 7.")
    parser.add_argument("-p", "--part", choices=("1", "2", "all"), default=str(PART))
    parser.add_argument("-i", "--input", default=INPUT)
    args = parser.parse_args()

    with open(args.input, mode="r", encoding="utf-8") as f:
        data = f.read()

    start = time.perf_counter()
    if args.part in ("1", "all"):
        print(f"Part 1: {prob_1(data)}")
    if args.part in ("2", "all"):
        print(f"Part 2: {prob_2(data)}")

    print(f"Time: {time.perf_counter() - start} s")
