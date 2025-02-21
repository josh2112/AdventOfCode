"""https://adventofcode.com/2018/day/3"""

import re
from dataclasses import dataclass
from itertools import combinations

from aoclib.runner import solve

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


@dataclass
class Claim:
    id: int
    x: int
    y: int
    w: int
    h: int


def overlap(a: Claim, b: Claim) -> int:
    if b.x < a.x:
        a, b = b, a
    x_overlap = max(0, a.x + a.w - b.x)
    if b.y < a.y:
        a, b = b, a
    y_overlap = max(0, a.y + a.h - b.y)
    return x_overlap * y_overlap


def prob_1(data: list[str]) -> int:
    claims = [
        Claim(*map(int, v))
        for v in re.findall(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)", "\n".join(data))
    ]
    return sum(overlap(*pr) for pr in combinations(claims, r=2))


def prob_2(data: list[str]) -> int:
    print(data)
    return 0


if __name__ == "__main__":
    solve(__file__, PART, INPUT, prob_1, prob_2)
