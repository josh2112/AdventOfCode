"""https://adventofcode.com/2025/day/12"""

from dataclasses import dataclass

from aoclib.runner import solve

# Input file path (or pass with -i <path>)
INPUT = "input.txt"

# Part to solve, 1 or 2 (or pass with -p <1|2|all>)
PART = 1

# Notes:
# - Each present is a 3x3 square. Stored with origin at center, coords will be (-1,-1) to (1,1)
# - Center does not change during rotate & flip
# - Precompute all orientations (rotations & flips). In case of symmetry remove duplicates
# - Present placement possibilities are (1,1) to (w-1,h-1) of each region
# - Trying all combos of present position and orientation is not workable...
#   Is there a trick, like figuring out present configs that make a rect and tiling them?
#   - In example, 0/2/0 and 3/5/3 both fit perfectly in 7x3. Can we use that?
# - Are there regions we can accept immediately (big enough that each present gets its own 3x3 square)?
#   - (w//3)*(h//3) >= present count
# - Are there regions we can reject immediately (not enough space for all present cells even disregarding shape)?
# - Turns out the last note is all we need.


@dataclass
class Present:
    cells: set[tuple[int, int]]


@dataclass
class Region:
    w: int
    h: int
    counts: list[int]


def prob_1(data: list[str]) -> int:
    div = [0] + [i + 1 for i, line in enumerate(data) if not line] + [len(data) + 1]
    *ps, rs = [data[a : b - 1] for a, b in zip(div, div[1:])]

    presents = [
        Present(
            {
                (x - 1, y - 1)
                for y, line in enumerate(lines[1:])
                for x, c in enumerate(line)
                if c == "#"
            },
        )
        for lines in ps
    ]

    regions = [
        Region(
            *map(int, line.split(":")[0].split("x")),
            list(map(int, line.split()[1:])),
        )
        for line in rs
    ]

    num_accepted = 0
    to_process = []

    # Pathological cases first:
    for r in regions:
        # Accept regions big enough that each present gets its own 3x3 square without complex fitting
        if (r.w // 3) * (r.h // 3) >= sum(r.counts):
            num_accepted += 1
        # Reject regions too small to fit all the presents even with perfect fitting. Store all others for further
        # processing.
        elif r.w * r.h >= sum(
            r.counts[i] * len(p.cells) for i, p in enumerate(presents)
        ):
            to_process.append(r)

    for r in to_process:
        # But it's empty... every region is either big enough that presents don't have to
        # share space, or too small that they can't fit even when shapes are not considered.
        pass

    return num_accepted


def prob_2(data: list[str]) -> int:
    return "Happy AoC 2025!"


if __name__ == "__main__":
    solve(__file__, PART, INPUT, prob_1, prob_2)
