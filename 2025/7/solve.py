"""https://adventofcode.com/2025/day/7"""

from dataclasses import dataclass, field
from functools import cache

from aoclib.runner import solve

# Input file path (or pass with -i <path>)
INPUT = "input.txt"

# Part to solve, 1 or 2 (or pass with -p <1|2|all>)
PART = 1


def prob_1(data: list[str]) -> int:
    beams = {data[0].index("S")}
    split_cnt = 0

    for line in data:
        for x, c in enumerate(line):
            if c == "^" and x in beams:
                beams.discard(x)
                beams.add(x - 1)
                beams.add(x + 1)
                split_cnt += 1

    return split_cnt


def prob_2_old(data: list[str]) -> int:
    timeline_cnt = 0

    # TODO: Not fast enough - takes 6 seconds on 80 rows, but full input is 140

    # Just for testing...
    data = data[:50]

    data.append("-" * len(data[0]))  # Sentinel row

    @cache
    def next_splitter(x: int, y: int) -> int:
        while data[y][x] == ".":
            y += 1
        return -1 if data[y][x] == "-" else y

    def trace(x: int, y: int):
        # Find next splitter or sentinel
        y = next_splitter(x, y)

        if y == -1:
            nonlocal timeline_cnt
            timeline_cnt += 1
            return

        trace(x - 1, y + 1)
        trace(x + 1, y + 1)

    trace(data[0].index("S"), 1)

    return timeline_cnt


def prob_2(data: list[str]) -> int:
    data.append("-" * len(data[0]))  # Sentinel row

    @dataclass
    class Node:
        parent: "Node | None" = None
        count: int = 0

    def build(x: int, y: int, parent: Node | None):
        if (x, y) not in nodes.keys():
            nodes[(x, y)] = Node(parent)
        n = nodes[(x, y)]

        while data[y][x] == ".":
            y += 1

        if data[y][x] == "^":
            build(x - 1, y + 1, n)
            build(x + 1, y + 1, n)

    nodes: dict[tuple[int, int], Node] = {}

    build(data[0].index("S"), 0, None)
    print(nodes)

    # TODO 1: Ensure tree built OK
    # TODO 2: Trace from bottom (1 level at a time) incrementing count on parent node

    return 0


if __name__ == "__main__":
    solve(__file__, PART, INPUT, prob_1, prob_2)
