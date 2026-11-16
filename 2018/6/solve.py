"""https://adventofcode.com/2018/day/6"""

from collections import Counter, defaultdict
from math import inf

from aoclib.runner import solve

# Input file path (or pass with -i <path>)
INPUT = "input.txt"

# Part to solve, 1 or 2 (or pass with -p <1|2|all>)
PART = 1

# Tricks:
# - Can we tell which points will be infinite? The leftmost, topmost, rightmost and bottommost points?
# - When calculating distances for a point in a row, stop when the point ceases to be the closest. It wont' be
#   again in that row. Ex. "aadddeccCc": we could stop computing d at index 5, once it's no longer the closest.


def print_grid(indices, xmin, xmax, ymin, ymax):
    grid = [["." for _ in range(xmax - xmin + 1)] for _ in range(ymax - ymin + 1)]
    for (x, y), i in indices.items():
        grid[y - ymin][x - xmin] = "abcdef"[i[0]] if len(i) == 1 else "."
    for row in grid:
        print("".join(str(c) for c in row))


# 4529 is not right...
def prob_1(data: list[str]) -> int:
    pts = [tuple(map(int, tuple(line.split(", ")))) for line in data]
    # Normalize row/col 0
    xmin, ymin = min(pt[0] for pt in pts), min(pt[1] for pt in pts)
    pts = [(pt[0] - xmin, pt[1] - ymin) for pt in pts]
    xmax, ymax = max(pt[0] for pt in pts), max(pt[1] for pt in pts)

    # (x,y) => dist to nearest point
    dists = defaultdict(lambda: inf)
    # (x,y) => list of indices nearest that point
    indices = defaultdict(list)

    for i, pt in enumerate(pts):
        for y in range(ymax + 1):
            for x in range(xmax + 1):
                new_dist = abs(pt[0] - x) + abs(pt[1] - y)
                if new_dist < dists[(x, y)]:
                    dists[(x, y)] = new_dist
                    indices[(x, y)] = [i]
                elif new_dist == dists[(x, y)]:
                    indices[(x, y)].append(i)

    tallies = Counter([lst[0] for lst in indices.values() if len(lst) == 1])

    # Discard any point with coords on an edge (those are infinite)
    for y in (0, ymax):
        for x in (0, xmax):
            for i in indices[(x, y)]:
                del tallies[i]

    return max(tallies.values())


def prob_2(data: list[str]) -> int:
    print(data)
    return 0


if __name__ == "__main__":
    solve(__file__, PART, INPUT, prob_1, prob_2)
