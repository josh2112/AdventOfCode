"""https://adventofcode.com/2016/day/14"""

import argparse
import itertools
import time
from hashlib import md5
from multiprocessing import Pool

# Input file path (default is "input.txt")
INPUT = "input.ex.txt"

# Part to solve, 1 or 2
PART = 1


def stretch_hash(i, salt, rehash):
    h = md5("".join((salt, str(i))).encode()).hexdigest()
    for x in range(rehash):
        h = md5(h.encode()).hexdigest()
    return h


def solve(salt: str, stretch: bool = False):
    i, num_keys = 0, 0
    possible_keys = []

    good_hash_numbers = []

    p = Pool()

    salt_array, stretch_array = (
        itertools.repeat(salt),
        itertools.repeat(2016 if stretch else 0),
    )

    hashes = []

    while True:
        if i == len(hashes):
            # Compute next 1000 "stretch" hashes in parallel
            hashes += p.starmap(
                stretch_hash,
                zip(range(i, 1000 + i), salt_array, stretch_array),
            )
        h = hashes[i]

        for t in [t for t in possible_keys if i - t[0] > 1000]:
            possible_keys.remove(t)

        quints = set(
            h[c]
            for c in range(len(h) - 5)
            if h[c] == h[c + 1] == h[c + 2] == h[c + 3] == h[c + 4]
        )

        for i0, k in possible_keys:
            if k in quints:
                num_keys += 1
                print(f"{i}: {h} contains key {k} (from hash #{i0})")
                good_hash_numbers = sorted(good_hash_numbers + [i0])
                # My input has a gotcha: The 64th key is actually found while looking at hash #22034, but those 64
                # include one (the 59th) that is found at a much later hash (#22065). Since the next key found is at a
                # lower hash (#22045), that would actually make it the 64th hash with a key. My stupid solution is,
                # once a 64th key is found, continue looking for a 64th key until we find one at a hash greater than the
                # first one was found, then return the lowest hash index found.
                if num_keys >= 64:
                    if i0 > good_hash_numbers[63]:
                        return good_hash_numbers[63]

        if k := next(
            (h[c] for c in range(2, len(h)) if h[c - 2] == h[c - 1] == h[c]), None
        ):
            possible_keys.append((i, k))

        i += 1


def prob_1(data: list[str]) -> int:
    return solve(data[0])


def prob_2(data: list[str]) -> int:
    return solve(data[0], stretch=True)  # 22034 too low??
    return 0


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2016 day 14.")
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
