"""https://adventofcode.com/2018/day/11"""

from aoclib.runner import solve

# Input file path (or pass with -i <path>)
INPUT = "input.txt"

# Part to solve, 1 or 2 (or pass with -p <1|2|all>)
PART = 1


def prob_1(data: list[str]) -> str:
    coord = doit(int(data[0]), [3])
    return ",".join(str(v) for v in coord[:2])


def prob_2(data: list[str]) -> str:
    coord = doit(int(data[0]), list(range(3, 20)))
    return ",".join(str(v) for v in coord)


def offsets(side: int):
    for y in range(side):
        for x in range(side):
            yield (x, y)


def doit(serial: int, valid_sizes: list[int]) -> tuple[int, int, int]:
    grid = [[0 for _ in range(301)] for _ in range(301)]

    for y in range(1, 301):
        for x in range(1, 301):
            rack_id = x + 10
            p = (rack_id * y + serial) * rack_id
            grid[y][x] = int((p / 100)) % 10 - 5

    max_p, max_coord = -100, (-1, -1, -1)

    for s in valid_sizes:
        sq = list(offsets(s))
        for y in range(1, 301 - s + 1):
            for x in range(1, 301 - s + 1):
                p = sum(grid[y + j][x + i] for i, j in sq)
                if p > max_p:
                    max_p = p
                    max_coord = (x, y, s)
                    print(max_coord, p)

    return max_coord


if __name__ == "__main__":
    solve(__file__, PART, INPUT, prob_1, prob_2)
