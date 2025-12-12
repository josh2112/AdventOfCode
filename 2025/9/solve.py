"""https://adventofcode.com/2025/day/9"""

from itertools import combinations

from aoclib.runner import solve

# Input file path (or pass with -i <path>)
INPUT = "input.txt"

# Part to solve, 1 or 2 (or pass with -p <1|2|all>)
PART = 1


def prob_1(data: list[str]) -> int:
    # Max area of rectangles made by all possible corner pairs
    return max(
        (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)
        for a, b in combinations([tuple(map(int, line.split(","))) for line in data], 2)
    )


def prob_2(data: list[str]) -> int:
    # Generate all corner pairs sorted by area descending
    # Take first pair with no edge intersections (i.e. each edge of figure is entirely on the same 'side' of the rectangle)

    corners = [tuple(map(int, line.split(","))) for line in data]
    edges = list(zip(corners, corners[1:] + [corners[0]]))

    pairs_by_size = {
        (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1): (a, b)
        for a, b in combinations([tuple(map(int, line.split(","))) for line in data], 2)
    }

    for size in sorted(pairs_by_size.keys(), reverse=True):
        a, b = pairs_by_size[size]
        x0, y0, x1, y1 = (
            min(a[0], b[0]),
            min(a[1], b[1]),
            max(a[0], b[0]),
            max(a[1], b[1]),
        )
        if all(
            (a[0] <= x0 and b[0] <= x0)
            or (a[0] >= x1 and b[0] >= x1)
            or (a[1] <= y0 and b[1] <= y0)
            or (a[1] >= y1 and b[1] >= y1)
            for a, b in edges
        ):
            print("FOUND IT!", a, b)
            return size


def main() -> float:
    return solve(__file__, PART, INPUT, prob_1, prob_2)


if __name__ == "__main__":
    main()
