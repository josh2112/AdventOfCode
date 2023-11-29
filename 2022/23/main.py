from recordclass import RecordClass
from typing import Union
import sys

SAMPLE = 0


def print_grid(r):
    allcoords = [k for k in elves]
    xmin, xmax = min(c[0] for c in allcoords), max(c[0] for c in allcoords)
    ymin, ymax = min(c[1] for c in allcoords), max(c[1] for c in allcoords)
    grid = [["." for _ in range(xmax - xmin + 1)] for _ in range(ymax - ymin + 1)]
    for k in elves:
        grid[k[1] - ymin][k[0] - xmin] = "#"
    print(f"== End of round {r} ==")
    for l in grid:
        print("".join(c for c in l))


class Elf(RecordClass):
    proposed: Union[tuple[int, int], None]


with open("input-sample.txt" if SAMPLE else "input.txt", "r") as f:
    elves: dict[tuple[int, int], Elf] = {}
    y = 0
    for line in f.readlines():
        for x in range(len(line)):
            if line[x] == "#":
                elves[(x, y)] = Elf(None)
        y += 1


adj = (
    (-1, -1),
    (0, -1),
    (1, -1),
    (-1, 0),
    (1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
)


dirs = (
    ((0, -1), set((adj[0], adj[1], adj[2]))),
    ((0, 1), set((adj[5], adj[6], adj[7]))),
    ((-1, 0), set((adj[0], adj[3], adj[5]))),
    ((1, 0), set((adj[2], adj[4], adj[7]))),
)


def main(partnum):
    d_idx = 0
    for r in range(10 if partnum == 1 else sys.maxsize):
        # First half of round
        for coord, elf in elves.items():
            elf.proposed = None
            occupied_dirs = set(d for d in adj if (coord[0] + d[0], coord[1] + d[1]) in elves)
            if occupied_dirs:
                for i in range(4):
                    dr = dirs[(d_idx + i) % 4]
                    if not dr[1].intersection(occupied_dirs):
                        elf.proposed = coord[0] + dr[0][0], coord[1] + dr[0][1]
                        # print(f"elf {coord} proposes {elf.proposed}")
                        break
            else:
                pass  # print(f"elf {coord} in the clear")

        if partnum == 2 and not next((1 for elf in elves.values() if elf.proposed), None):
            print(f"Round {r+1}, no elves moving")
            return

        # Second half of round
        seen = set()
        proposed = (elf.proposed for elf in elves.values() if elf.proposed)
        dupes = set((c for c in proposed if c in seen or seen.add(c)))
        for coord, elf in elves.copy().items():
            if elf.proposed and elf.proposed not in dupes:
                elves[elf.proposed] = elf
                # print(f"elf {coord} moves to proposed ({elf.proposed})")
                del elves[coord]
            else:
                pass  # print(f"elf {coord} can't move (dupe)")

        # End of round
        d_idx += 1
        # print_grid(r + 1)

    allcoords = [k for k in elves]
    xmin, xmax = min(c[0] for c in allcoords), max(c[0] for c in allcoords)
    ymin, ymax = min(c[1] for c in allcoords), max(c[1] for c in allcoords)
    empty = 0
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            if not (x, y) in allcoords:
                empty += 1
    print("Empty tiles:", empty)


main(2)
