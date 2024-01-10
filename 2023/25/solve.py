"""https://adventofcode.com/2023/day/25"""

import argparse
from collections import defaultdict
import dataclasses
import random
import time
import itertools
from typing import Union

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


@dataclasses.dataclass
class Node:
    name: str
    visited: bool = False
    prev: Union["Node", None] = None


def parse(data: list[str]):
    lines = [line.split() for line in data]
    edges = [(line[0][:-1], endpt) for line in lines for endpt in line[1:]]
    nodes = [Node(n) for n in set(a for pr in edges for a in pr)]
    return nodes, [
        (
            next(n for n in nodes if n.name == e[0]),
            next(n for n in nodes if n.name == e[1]),
        )
        for e in edges
    ]


class Visitor:
    def __init__(self, nodes, edges):
        self.nodes, self.edges = nodes, edges

    def pathfind_bfs(self, a: Node, b: Node):
        q = []
        for n in self.nodes:
            n.visited = False
            n.prev = None
        a.visited = True
        q.append(a)
        while q:
            v = q.pop(0)
            if v == b:
                return v
            for e in [e for e in self.edges if v in e]:
                w = e[1] if e[0] == v else e[0]
                if not w.visited:
                    w.visited = True
                    w.prev = v
                    q.append(w)

    def visit_all(self, s: Node):
        q = []
        for n in self.nodes:
            n.visited = False
        s.visited = True
        q.append(s)
        while q:
            v = q.pop(0)
            for e in [e for e in self.edges if v in e]:
                w = e[1] if e[0] == v else e[0]
                if not w.visited:
                    w.visited = True
                    q.append(w)


# Stochastically "solve" by tracing paths between a bunch of random pairs
# of nodes. If everything goes well, the 3 edges we're looking for will
# have been used way more than the rest. Slow, but no dependencies!
def prob_1(data: list[str]):
    nodes, edges = parse(data)

    v = Visitor(nodes, edges)
    edgecnt: dict[tuple[str, str], int] = defaultdict(int)

    combos = random.sample(list(itertools.combinations(nodes, 2)), 100)
    i = 0

    for a, b in combos:
        i += 1
        print(f"Checking {i}/{len(combos)}", end="\r")
        dest = v.pathfind_bfs(a, b)
        n = dest
        path = []
        while n:
            path.append(n)
            n = n.prev
            if n:
                e0, e1 = sorted([path[-1].name, n.name])
                edgecnt[(e0, e1)] += 1

    edges_by_cnt = sorted(edgecnt.keys(), key=lambda e: edgecnt[e], reverse=True)
    for e in edges_by_cnt[:3]:
        edges.remove(
            next(
                ed
                for ed in edges
                if e[0] in (ed[0].name, ed[1].name) and e[1] in (ed[0].name, ed[1].name)
            )
        )
    # group 1 = all nodes connected to first node
    # group 2 = all nodes connected to (pick a node not in group 1)
    # sanity check: ensure group 1 + group 2 = len(nodes)
    v = Visitor(nodes, edges)
    v.visit_all(nodes[0])
    g1 = [n for n in v.nodes if n.visited]
    if len(g1) == len(nodes):
        print("Fail: graph not divided")
        return None
    n = next(n for n in v.nodes if not n.visited)
    v.visit_all(n)
    g2 = [n for n in v.nodes if n.visited]
    print("Group sizes:", len(g1), len(g2))
    return len(g1) * len(g2)


def prob_2(_data: list[str]):
    return "Freebie!"


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2023 day 25.")
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
