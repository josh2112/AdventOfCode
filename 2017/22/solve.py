"""https://adventofcode.com/2017/day/22"""

from collections import defaultdict

from aoclib.runner import solve

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1

DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def parse(data: list[str]):
    return (
        w := len(data[0]),
        h := len(data),
        defaultdict(
            lambda: ".",
            {
                (x - w // 2, y - h // 2): "#"
                for y in range(h)
                for x in range(w)
                if data[y][x] == "#"
            },
        ),
    )


def prob_1(data: list[str]) -> int:
    w, h, grid = parse(data)
    p, d = (0, 0), 0
    num_rounds_infection = 0

    for _ in range(10_000):
        state = grid[p]

        match state:
            case "#":
                dd = 1
                grid[p] = "."
            case ".":
                dd = -1
                grid[p] = "#"
                num_rounds_infection += 1

        d = (d + dd) % len(DIRS)
        p = (p[0] + DIRS[d][0], p[1] + DIRS[d][1])

    return num_rounds_infection


def prob_2(data: list[str]) -> int:
    w, h, grid = parse(data)
    p, d = (0, 0), 0
    num_rounds_infection = 0

    for _ in range(10_000_000):
        state = grid[p]

        match state:
            case "#":
                dd = 1
                grid[p] = "F"
            case "W":
                dd = 0
                grid[p] = "#"
                num_rounds_infection += 1
            case "F":
                dd = 2
                grid[p] = "."
            case ".":
                dd = -1
                grid[p] = "W"

        d = (d + dd) % len(DIRS)
        p = (p[0] + DIRS[d][0], p[1] + DIRS[d][1])

    return num_rounds_infection


if __name__ == "__main__":
    solve(__file__, PART, INPUT, prob_1, prob_2)
