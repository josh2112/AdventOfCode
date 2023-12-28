#!/usr/bin/env python3

from collections import defaultdict
import dataclasses
import random
import time
import itertools
from typing import Union

# https://adventofcode.com/2023/day/25

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


def prob_1(data: list[str]):
    nodes, edges = parse(data)

    v = Visitor(nodes, edges)
    edgecnt: dict[tuple[str, str], int] = defaultdict(int)

    combos = random.sample(list(itertools.combinations(nodes, 2)), 100)
    print("Num pairs to check:", len(combos))
    i = 0

    for a, b in combos:
        i += 1
        # if not (i % 100):
        print("Checked", i)
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


def prob_2(data: list[str]):
    print(data)


def main():
    with open(INPUT or "input.txt", mode="r", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    start = time.perf_counter()
    result = prob_1(data) if PART == 1 else prob_2(data)
    elapsed = time.perf_counter() - start

    print(f"Problem {PART}: {result}")
    print(f"Time: {elapsed} s")


if __name__ == "__main__":
    main()
