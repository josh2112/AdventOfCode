import re
import numpy

USE_SAMPLE = 0
PART = 2

with open("input-sample.txt" if USE_SAMPLE else "input.txt", "r") as f:
    coords = [
        ((int(p[0]), int(p[1])), (int(p[2]), int(p[3])))
        for p in [re.findall(r"[x|y]=(-?\d+)", l) for l in f.readlines()]
    ]


def coverage(c, d):
    # Return all coordinates that satisfy manhattan distance
    for y in range(-d, d + 1):
        for x in range(-(d - abs(y)), d - abs(y) + 1):
            yield c[0] + x, c[1] + y


def part1():
    row = 10 if USE_SAMPLE else 2000000
    grid = {}

    for s, b in coords:
        grid[s] = "S"
        grid[b] = "B"

    for s, b in coords:
        d = abs(s[0] - b[0]) + abs(s[1] - b[1])
        if s[1] - d <= row and s[1] + d >= row:
            dy = abs(row - s[1])
            for x in range(-(d - abs(dy)), d - abs(dy) + 1):
                c = s[0] + x, row
                if not c in grid:
                    grid[c] = "#"

    empty = len([m for c, m in grid.items() if c[1] == row and m == "#"])
    print(empty)


def part2():
    MAX = (20 if USE_SAMPLE else 4000000) + 1
    mhdist = lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1])

    # arr = [["." for i in range(21)] for j in range(21)]
    # solutions = []

    sdist = [(s, mhdist(s, b)) for s, b in coords]

    for y in range(MAX):
        if not y % 100000:
            print(y)
        # Calculate the ranges each sensor's search area on this row
        ranges = []
        for s, d in sdist:
            if s[1] - d <= y and s[1] + d >= y:
                dy = abs(y - s[1])
                ranges.append(range(s[0] + -(d - abs(dy)), s[0] + d - abs(dy) + 1))
        ranges = list(sorted(ranges, key=lambda r: r.start))

        # for i in range(len(ranges)):
        #    for x in ranges[i]:
        #        if x >= 0 and x < 21:
        #            arr[y][x] = "#"

        x = 0
        for i in range(len(ranges) - 1):
            if x in ranges[i]:
                x = ranges[i].stop
            elif ranges[i].start > x:
                print("FOUND IT:", (x, y), " => ", (x * 4000000 + y))
                return
                # solutions.append((x, y))

    # for s, d in sdist:
    #    arr[s[1]][s[0]] = "S"

    # print("\n".join(["".join(l) for l in arr]))
    # print(solutions)


part1() if PART == 1 else part2()
