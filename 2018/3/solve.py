"""https://adventofcode.com/2018/day/3"""

import re
from itertools import combinations, product

from aoclib.runner import solve

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


class Claim:
    def __init__(self, id, x, y, w, h):
        self.id, self.x, self.y, self.w, self.h = id, x, y, w, h
        self.r, self.b = self.x + self.w, self.y + self.h


def parse_claims(data: list[str]) -> list[Claim]:
    return [
        Claim(*map(int, v))
        for v in re.findall(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)", "\n".join(data))
    ]


def build_cloth(claims: list[Claim]):
    xmax, ymax = max(c.r for c in claims), max(c.b for c in claims)
    cloth = [0] * xmax * ymax
    for a, b in combinations(claims, r=2):
        if b.x < a.x:
            a, b = b, a
        xspan = range(b.x, min(a.r, b.r))
        if b.y < a.y:
            a, b = b, a
        yspan = range(b.y, min(a.b, b.b))
        for x, y in product(xspan, yspan):
            cloth[x + y * xmax] = 1
    return cloth


def prob_1(data: list[str]) -> int:
    return sum(build_cloth(parse_claims(data)))


def prob_2(data: list[str]) -> int:
    claims = parse_claims(data)
    xmax = max(c.r for c in claims)
    cloth = build_cloth(claims)
    condition = lambda c: all(
        cloth[x + y * xmax] == 0 for y in range(c.y, c.b) for x in range(c.x, c.r)
    )
    return next(c for c in claims if condition(c)).id


if __name__ == "__main__":
    solve(__file__, PART, INPUT, prob_1, prob_2)
