"""https://adventofcode.com/2023/day/22"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 2


# Generate names A..Z, AA..ZZ, AAA... etc.
def names():
    for i in range(26):
        yield chr(ord("A") + i)
    for j in range(26):
        for i in range(26):
            yield f"{chr(ord('A') + j)}{chr(ord('A') + i)}"
    for k in range(26):
        for j in range(26):
            for i in range(26):
                yield f"{chr(ord('A') + k)}{chr(ord('A') + j)}{chr(ord('A') + i)}"


class Brick:
    def __init__(self, name: str, c1: list[int], c2: list[int]):
        self.name = name
        self.x = range(min(c1[0], c2[0]), max(c1[0], c2[0]) + 1)
        self.y = range(min(c1[1], c2[1]), max(c1[1], c2[1]) + 1)
        self.z = range(min(c1[2], c2[2]), max(c1[2], c2[2]) + 1)

    def __repr__(self) -> str:
        return f"{self.name}: {self.x.start},{self.y.start},{self.z.start}~{self.x.stop-1},{self.y.stop-1},{self.z.stop-1}"

    def intersect_horiz(self, other: "Brick"):
        return (self.x.start < other.x.stop and other.x.start < self.x.stop) and (
            self.y.start < other.y.stop and other.y.start < self.y.stop
        )


def setup(data: list[str]):
    points = [
        [[int(x) for x in p.split(",")] for p in line.split("~")] for line in data
    ]

    bricks = sorted(
        (Brick(n, ps[0], ps[1]) for n, ps in zip(names(), points)),
        key=lambda b: b.z.start,
    )
    xmax = max(b.x.stop for b in bricks)
    ymax = max(b.y.stop for b in bricks)
    zmax = max(b.z.stop for b in bricks) + 1

    base = Brick("_", [0, 0, 0], [xmax - 1, ymax - 1, 0])

    brick_tops = {
        z: [b for b in bricks + [base] if z == b.z.stop - 1] for z in range(zmax)
    }
    brick_bottoms = {
        z: [b for b in bricks + [base] if z == b.z.start] for z in range(zmax)
    }

    for b in bricks:
        # check the x,y rect of this brick from just under it until we hit another brick
        for z in range(b.z.start - 1, -1, -1):
            if any(bt.intersect_horiz(b) for bt in brick_tops[z]):
                # How far do we need to move it down?
                dz = b.z.start - (z + 1)
                if dz > 0:
                    # Correct the top and bottom
                    brick_bottoms[b.z.start].remove(b)
                    brick_bottoms[b.z.start - dz].append(b)
                    brick_tops[b.z.stop - 1].remove(b)
                    brick_tops[b.z.stop - 1 - dz].append(b)
                    b.z = range(b.z.start - dz, b.z.stop - dz)
                break

    # supporters[C] = [A,B] means C is supported by A and B
    supporters: dict[Brick, set[Brick]] = {}

    # supporting[A] = [B,C] means A supports B and C
    supporting: dict[Brick, set[Brick]] = {}

    for b in bricks:
        # Find all the bricks whose top x/y rect is right below the bottom of this one
        supporters[b] = set(
            br for br in brick_tops[b.z.start - 1] if br.intersect_horiz(b)
        )
        # Find all the bricks whose bottom x/y rect is right above top of this one
        supporting[b] = set(
            br for br in brick_bottoms[b.z.stop] if br.intersect_horiz(b)
        )

    # Remove a brick if it doesn't support any others or all bricks supported by it are each
    # supported by more than 1 brick
    to_be_removed = [
        b for b in bricks if all(len(supporters[above]) > 1 for above in supporting[b])
    ]

    return bricks, to_be_removed, supporting, supporters


def prob_1(data: list[str]):
    _, to_be_removed, _, _ = setup(data)
    return len(to_be_removed)


def prob_2(data: list[str]):
    bricks, to_be_removed, supporting, supporters = setup(data)

    fall_cnt = {}
    for a in set(bricks) - set(to_be_removed):
        fallers = set()
        aboves = set(b for b in supporting[a] if not supporters[b] - set([a]))
        fallers.update(aboves)
        while aboves:
            # For each of these bricks, grab the bricks on top that are only being supported by
            # bricks that have fallen so far
            aboves = set(
                c
                for b in aboves
                for c in supporting[b]
                if not (supporters[c] - fallers)
            )
            fallers.update(aboves)
        fall_cnt[a] = fallers

    return sum(len(f) for f in fall_cnt.values())


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2023 day 22.")
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
