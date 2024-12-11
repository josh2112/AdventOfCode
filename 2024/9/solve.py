"""https://adventofcode.com/2024/day/9"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.ex.txt"

# Part to solve, 1 or 2
PART = 2


def printdisk(disk):
    print("".join("." if c < 0 else str(c) for c in disk))


def prob_1(data: list[str]) -> int:
    disk = []
    is_file, file_id = True, 0
    for v in data[0]:
        disk += [-1 if not is_file else file_id] * int(v)
        if is_file:
            file_id += 1
        is_file = not is_file
    p1, p2 = 0, len(disk) - 1
    while True:
        while disk[p1] >= 0:
            p1 += 1
        while disk[p2] < 0:
            p2 -= 1
        if p1 >= p2:
            break
        disk[p1], disk[p2] = disk[p2], disk[p1]

    return sum(d * i if d >= 0 else 0 for i, d in enumerate(disk))


def prob_2(data: list[str]) -> int:
    free, file = [], []
    is_file, file_id = True, 0
    start = 0
    for v in data[0]:
        length = int(v)
        if length:
            if is_file:
                file.append((file_id, start, length))
                file_id += 1
            else:
                free.append((start, length))
        is_file = not is_file
        start += length

    pfile = len(file) - 1
    while pfile >= 0:
        fid, fstart, flen = file[pfile]
        pfree = next((pfree for pfree in free if pfree[1] >= flen), None)
        # Is there a block to the left of the file big enough?
        if pfree and pfree[0] < fstart:
            # Move the file
            file[pfile] = (fid, pfree[0], flen)
            if pfree[1] == flen:
                # Remove the free block if the file takes up the whole block
                free.remove(pfree)
            else:
                # Shrink the free block down to the remaining free space (file on left, remnants of free block on right)
                free[free.index(pfree)] = (pfree[0] + flen, pfree[1] - flen)

            # The space where the file was is now free
            free.append((fstart, flen))

            file = sorted(file)
            free = sorted(free)

            # TODO: If we move a file and there was free space on either side of it, we now have 2 or 3 contiguous free
            # spaces that need to be combined. We're not doing that now, and probably missing file moves.
            # Find the index of the new free area in the now-sorted free block list and check the adjacent areas. Can
            # they be combined?
            # TODO: This doesn't change the answer at all. Doubelc check it.

            # Compact free space (e.g. (3,2), (5,1), (6,4) => (3,7))

            i = free.index((fstart, flen))
            if i > 0:
                if free[i - 1][0] + free[i - 1][1] == free[i][0]:
                    free[i] = (free[i - 1][0], free[i - 1][1] + free[i][1])
                    del free[i - 1]
                    i -= 1
            if i < len(free) - 1:
                if free[i][0] + free[i][1] == free[i + 1][0]:
                    free[i] = (free[i][0], free[i][1] + free[i + 1][1])
                    del free[i + 1]

            # print(f"---[{fid}]---")
            # print("files = ", file)
            # print("free =", free)
        pfile -= 1

    # 9963020502985 is too high? count of file blocks is the same and there are no overlaps or gaps in ranges...
    return sum(
        sum(i * fid for i in range(fstart, fstart + flen)) for fid, fstart, flen in file
    )


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2024 day 9.")
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
