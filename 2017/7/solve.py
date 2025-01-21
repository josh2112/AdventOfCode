"""https://adventofcode.com/2017/day/7"""

import argparse
import re
import time
from collections import Counter

# Input file path (default is "input.txt")
INPUT = "input.ex.txt"

# Part to solve, 1 or 2
PART = 2


def parse(data: str):
    for name, weight, children in re.findall(
        r"(\w+) \((\d+)\)(?: -> )?([\w, ]+)?", data
    ):
        yield name, int(weight), children.split(", ") if children else []


def find_root(progs):
    cur = progs[0]
    while True:
        parent = next((p for p in progs if cur[0] in p[2]), None)
        if not parent:
            return cur
        cur = parent


def prob_1(data: str) -> int:
    progs = list(parse(data))
    return find_root(progs)[0]


def fill_weights(node, progmap):
    weight = node[1] + sum(fill_weights(progmap[c], progmap) for c in node[2])
    progmap[node[0]] = (node[0], node[1], node[2], weight)
    return weight


def write_graphviz(progs):
    with open("graph.dot", "w") as f:
        f.write("graph {\n")
        for n in progs.values():
            f.write(f'  {n[0]} [label="{n[0]} {n[1]}\\n{n[3]}"]\n')
        for n in progs.values():
            for c in n[2]:
                f.write(f"  {n[0]} -- {c}\n")
        f.write("}\n")


def prob_2(data: list[str]) -> int:
    progs = list(parse(data))
    root = find_root(progs)
    progmap = {p[0]: p for p in progs}
    fill_weights(root, progmap)

    unbalanced = [
        p for p in progmap.values() if len(set([progmap[c][3] for c in p[2]])) > 1
    ]
    for u in unbalanced:
        print(
            f"{u[0]} = {u[1]} + {', '.join(f'{c} ({progmap[c][1]})' for c in u[2])} = {u[3]}"
        )

    unbalanced = sorted(
        [
            progmap[p]
            for p in next(
                p
                for p in progmap.values()
                if len(set([progmap[c][3] for c in p[2]])) > 1
            )[2]
        ],
        key=lambda p: p[3],
    )
    bad, good = (
        (unbalanced[-1], unbalanced[0])
        if unbalanced[0][3] == unbalanced[1][3]
        else (unbalanced[0], unbalanced[-1])
    )
    return bad[1] - (bad[3] - good[3])


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
