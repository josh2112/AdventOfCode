"""https://adventofcode.com/2018/day/6"""

from collections import Counter, defaultdict
from math import inf

from aoclib.runner import solve

# Input file path (or pass with -i <path>)
INPUT = "input.txt"

# Part to solve, 1 or 2 (or pass with -p <1|2|all>)
PART = 1


def preprocess(data: list[str]) -> tuple[list[tuple[int, int]], int, int]:
    pts = [tuple(map(int, tuple(line.split(", ")))) for line in data]

    # Normalize row/col 0
    xmin, ymin = min(pt[0] for pt in pts), min(pt[1] for pt in pts)
    pts = [(pt[0] - xmin, pt[1] - ymin) for pt in pts]

    return pts, max(pt[0] for pt in pts) + 1, max(pt[1] for pt in pts) + 1


def prob_1(data: list[str]) -> int:
    pts, w, h = preprocess(data)

    # (x,y) => dist to nearest point
    dists = defaultdict(lambda: inf)
    # (x,y) => list of indices nearest that point
    indices = defaultdict(list)

    for i, pt in enumerate(pts):
        for y in range(h):
            for x in range(w):
                new_dist = abs(pt[0] - x) + abs(pt[1] - y)
                if new_dist < dists[(x, y)]:
                    dists[(x, y)] = new_dist
                    indices[(x, y)] = [i]
                elif new_dist == dists[(x, y)]:
                    indices[(x, y)].append(i)

    tallies = Counter([lst[0] for lst in indices.values() if len(lst) == 1])

    # Discard any point with coords on an edge (those are infinite)
    for x in (0, w - 1):
        for y in range(h):
            for i in indices[(x, y)]:
                del tallies[i]
    for y in (0, h - 1):
        for x in range(w):
            for i in indices[(x, y)]:
                del tallies[i]

    return max(tallies.values())


def prob_2(data: list[str]) -> int:
    pts, w, h = preprocess(data)

    target = 10_000 if len(pts) > 10 else 32
    region_size = 0

    for x in range(w):
        for y in range(h):
            if sum(abs(px - x) + abs(py - y) for px, py in pts) < target:
                region_size += 1

    return region_size


if __name__ == "__main__":
    solve(__file__, PART, INPUT, prob_1, prob_2)
