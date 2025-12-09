"""https://adventofcode.com/2025/day/9"""

from itertools import combinations

from aoclib.runner import solve

# Input file path (or pass with -i <path>)
INPUT = "input.txt"

# Part to solve, 1 or 2 (or pass with -p <1|2|all>)
PART = 1


def prob_1(data: list[str]) -> int:
    return max(
        (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)
        for a, b in combinations([tuple(map(int, line.split(","))) for line in data], 2)
    )


def _make_border(data: list[str]) -> set[tuple[int, int]]:
    # Possible approach: building a set of cells on the perimeter. Takes over a second with real input though.
    border = set()
    corners = [tuple(map(int, line.split(","))) for line in data]
    for a, b in zip(corners, corners[1:] + [corners[0]]):
        for i in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
            border.add((i, a[1]))
        for i in range(min(a[1], b[1]), max(a[1], b[1]) + 1):
            border.add((a[0], i))
    return border


# It's between 631896752 and 4636745093
def prob_2(data: list[str]) -> int:
    # For each tile corner pair, calculate other 2 corners and ensure they are within the figure

    corners = [tuple(map(int, line.split(","))) for line in data]
    edges = [
        (b, a) if a[0] + a[1] > b[0] + b[1] else (a, b)
        for a, b in list(zip(corners, corners[1:] + [corners[0]]))
    ]
    v_edges = [(a, b) for a, b in edges if a[0] == b[0]]

    def is_point_inside(c: tuple[int, int]) -> bool:
        # First, are we on an edge (because this screws up the crossing count)?
        return any(
            e
            for e in edges
            if (e[0][0] == c[0] and e[0][1] <= c[1] <= e[1][1])
            or (e[0][1] == c[1] and e[0][0] <= c[0] <= e[1][0])
        ) or (
            # To test inside the figure, shoot a line to the left and count vertical edge crossings. Odd = inside.
            sum(
                1
                for x in range(c[0] + 1)
                for e in v_edges
                if e[0][0] == x and e[0][1] <= c[1] < e[1][1]
            )
            % 2
            == 1
        )

    def check_interior(x0: int, y0: int, x1: int, y1: int) -> bool:
        for a, b in edges:
            if (x0 < a[0] < x1 and y0 < a[1] < y1) or (
                x0 < b[0] < x1 and y0 < b[1] < y1
            ):
                return False
        return True

    # Calculate the area of each possible rectangle
    pairs_by_size = {
        (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1): (a, b)
        for a, b in combinations([tuple(map(int, line.split(","))) for line in data], 2)
    }
    # Check rectangles in order of size, returning the first valid one
    for size in sorted(pairs_by_size.keys(), reverse=True):
        a, b = pairs_by_size[size]
        if is_point_inside((a[0], b[1])) and is_point_inside((b[0], a[1])):
            print("FOUND IT!", a, b)
            return size

    dmax = 0
    for a, b in combinations([tuple(map(int, line.split(","))) for line in data], 2):
        if (
            (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1) > dmax
            and is_point_inside((a[0], b[1]))
            and is_point_inside((b[0], a[1]))
            # Great, but we can have all 4 corners inside the figure and still have a huge gash cutting across it!
            # Make sure we don't have any edges starting or ending inside our rectangle
            and check_interior(
                min(a[0], b[0]),
                min(a[1], b[1]),
                max(a[0], b[0]),
                max(a[1], b[1]),
            )
        ):
            dmax = (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)
            print(dmax)
    return dmax


if __name__ == "__main__":
    solve(__file__, PART, INPUT, prob_1, prob_2)
