"""https://adventofcode.com/2025/day/7"""

from collections import defaultdict
from dataclasses import dataclass, field

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


def prob_2(data: list[str]) -> int:
    # Start with a row of all 1's
    # For each row from the bottom:
    #  - Where ^ found, sum the two adjacents

    counts = [1 for _ in range(len(data[0]))]

    for line in reversed(data):
        for x in [x for x, c in enumerate(line) if c == "^"]:
            counts[x] = counts[x - 1] + counts[x + 1]

    return counts[data[0].index("S")]


if __name__ == "__main__":
    solve(__file__, PART, INPUT, prob_1, prob_2)
