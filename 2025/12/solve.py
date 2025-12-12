"""https://adventofcode.com/2025/day/12"""

from aoclib.runner import solve
from dataclasses import dataclass

# Input file path (or pass with -i <path>)
INPUT = "input.txt"

# Part to solve, 1 or 2 (or pass with -p <1|2|all>)
PART = 1

# Notes:
# - Each present is a 3x3 square. Stored with origin at center, coords will be (-1,-1) to (1,1)
# - Center does not change during rotate & flip
# - Precompute all unique orientations (rotations & flips)
# - Present origin possibilities are (1,1) to (w-1,h-1) of each region
# - Trying all combos of present position and orientation is not workable...
#   Is there a trick, like figuring out present configs that make a rect and tiling them?
# - Are there cases we can accept immediately (region is big enough that each present gets its own 3x3 square)?
#   - (w//3)*(h//3) >= present count


@dataclass
class Present:
    i: int
    cells: list[tuple[int, int]]

    @staticmethod
    def from_lines(lines: list[str]) -> "Present":
        return Present(
            int(lines[0].split(":")[0]),
            [
                (x, y)
                for y, line in enumerate(lines[1:])
                for x, c in enumerate(line)
                if c == "#"
            ],
        )


@dataclass
class Region:
    size: tuple[int, int]
    counts: list[int]

    @staticmethod
    def from_line(line: str) -> "Region":
        tokens = line.split()
        return Region(
            tuple(map(int, tokens[0][:-1].split("x"))),
            list(map(int, tokens[1:])),
        )


def prob_1(data: list[str]) -> int:
    div = [0] + [i + 1 for i, line in enumerate(data) if not line] + [len(data) + 1]
    *ps, rs = [data[a : b - 1] for a, b in zip(div, div[1:])]
    presents = [Present.from_lines(p) for p in ps]
    regions = [Region.from_line(r) for r in rs]

    easy_regions = [
        r for r in regions if (r.size[0] // 3) * (r.size[1] // 3) >= sum(r.counts)
    ]
    regions = set(regions) - set(easy_regions)
    return len(easy_regions)


def prob_2(data: list[str]) -> int:
    print(data)
    return 0


if __name__ == "__main__":
    solve(__file__, PART, INPUT, prob_1, prob_2)
