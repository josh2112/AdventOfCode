"""https://adventofcode.com/2024/day/12"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.ex1.txt"

# Part to solve, 1 or 2
PART = 1


def parse(data: list[str]):
    border = [(".", -1)]
    return [
        border * (len(data[0]) + 2),
        *[border + [[p, -1] for p in line] + border for line in data],
        border * (len(data[0]) + 2),
    ]


def griditer(xstart, xstop, ystart, ystop):
    for y in range(ystart, ystop):
        for x in range(xstart, xstop):
            yield x, y


def flood_fill(garden, x, y, pid):
    ltr = garden[y][x][0]
    q = [(x, y)]
    area, perimeter = 0, 0
    while q:
        p = q.pop(0)
        area += 1
        garden[p[1]][p[0]][1] = pid
        neighbors = [
            (p[0] + d[0], p[1] + d[1]) for d in ((-1, 0), (1, 0), (0, -1), (0, 1))
        ]
        perimeter += 4 - sum(
            1 if garden[n[1]][n[0]][0] == ltr else 0 for n in neighbors
        )
        for n in neighbors:
            if n not in q and garden[n[1]][n[0]] == [ltr, -1]:
                q.append(n)
    # print(f"{ltr} {(x,y)}: perim {perimeter}, area {area}")
    return area, perimeter


def flood_fill_sides(garden, x, y, pid):
    ltr = garden[y][x][0]
    q = [(x, y)]
    area, num_sides = 0, 0
    while q:
        p = q.pop(0)
        area += 1
        garden[p[1]][p[0]][1] = pid
        # List of
        neighbors = [
            garden[p[1] + d[1]][p[0] + d[0]][0] == ltr
            for d in (
                (0, -1),
                (1, -1),
                (1, 0),
                (1, 1),
                (0, 1),
                (-1, 1),
                (-1, 0),
                (-1, -1),
            )
        ]
        outside = sum(
            1 if not (neighbors[a] or neighbors[b]) else 0
            for a, b in ((0, 2), (2, 4), (4, 6), (6, 0))
        )
        inside = sum(
            1 if neighbors[a] and neighbors[b] and not neighbors[c] else 0
            for a, b, c in ((0, 2, 1), (2, 4, 3), (4, 6, 5), (6, 0, 7))
        )
        num_sides += outside + inside

        for n in [
            (p[0] + d[0], p[1] + d[1]) for d in ((-1, 0), (1, 0), (0, -1), (0, 1))
        ]:
            if n not in q and garden[n[1]][n[0]] == [ltr, -1]:
                q.append(n)

    # print(f"{ltr} {(x,y)}: area {area}, {num_sides} sides")
    return area, num_sides


def segment(garden, fill_algo):
    num_plots = 0
    price = 0
    for x, y in griditer(1, len(garden[0]) - 1, 1, len(garden) - 1):
        if garden[y][x][1] == -1:
            a, p = fill_algo(garden, x, y, num_plots)
            price += a * p
            num_plots += 1
    return price


def prob_1(data: list[str]) -> int:
    garden = parse(data)
    return segment(garden, flood_fill)


def prob_2(data: list[str]) -> int:
    garden = parse(data)
    return segment(garden, flood_fill_sides)


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2024 day 12.")
    parser.add_argument("-p", "--part", choices=("1", "2", "all"), default=str(PART))
    parser.add_argument("-i", "--input", default=INPUT)
    args = parser.parse_args()
    part, infile = args.part, args.input

    with open(infile, mode="r", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    start = time.perf_counter()
    if part in ("1", "all"):
        print(f"Part 1: {prob_1(data)}")
    if part in ("2", "all"):
        print(f"Part 2: {prob_2(data)}")

    elapsed = time.perf_counter() - start
    print(f"Time: {elapsed} s")

    return elapsed


if __name__ == "__main__":
    main()
