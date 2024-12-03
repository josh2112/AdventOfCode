"""https://adventofcode.com/2016/day/11"""

import argparse
import heapq
import itertools
import time
from string import ascii_uppercase

# Input file path (default is "input.txt")
INPUT = "input.ex.txt"

# Part to solve, 1 or 2
PART = 1


def parse(data: list[str]) -> list[set[str]]:
    floors = []
    types, i = {}, 0
    for line in data:
        tk = line.replace(",", "").replace(".", "").split()
        generators = [tk[i - 1] for i, t in enumerate(tk) if t == "generator"]
        microchips = [
            tk[i - 1].split("-")[0] for i, t in enumerate(tk) if t == "microchip"
        ]
        for t in generators + microchips:
            if t not in types:
                types[t] = ascii_uppercase[i]
                i += 1
        floors.append(
            set(
                [types[t] + "G" for t in generators]
                + [types[t] + "M" for t in microchips]
            )
        )
    return floors


def encode(floors):
    chips, gens = {}, {}
    for i, f in enumerate(floors):
        for item in f:
            if item[1] == "M":
                chips[item[0]] = i
            else:
                gens[item[0]] = i
    return list(sorted((chips[k], gens[k]) for k in chips))


def decode(pairs):
    floors = [set(), set(), set(), set()]
    for i in range(len(pairs)):
        ltr = ascii_uppercase[i]
        floors[pairs[i][0]].add(ltr + "M")
        floors[pairs[i][1]].add(ltr + "G")
    return floors


def is_floor_valid(floor) -> bool:
    mc = set(i[0] for i in floor if i[1] == "M")
    gen = set(i[0] for i in floor if i[1] == "G")
    return not gen or not mc.difference(gen)


def run(floors) -> int:
    elev = 0

    q = [(0, elev, encode(floors))]
    visited = [q[0]]

    while q:
        steps, elev, floorcodes = state = heapq.heappop(q)
        # print(f"From state {state}:")
        floors = decode(floorcodes)

        if all(f == (3, 3) for f in floorcodes):
            return steps

        nextstates = []

        # What can the elevator carry from this floor?
        for payload in [(x,) for x in floors[elev]] + list(
            itertools.combinations(floors[elev], 2)
        ):
            # What floors can this payload go to?
            valid_floors = []
            for f in range(elev + 1, 4):
                if is_floor_valid(set(payload).union(floors[f])):
                    valid_floors.append(f)
                else:
                    break
            for f in range(elev - 1, -1, -1):
                if is_floor_valid(set(payload).union(floors[f])):
                    valid_floors.append(f)
                else:
                    break
            # Make a state for each of the floor/payload combinations
            for dest in valid_floors:
                result = set(payload).union(floors[dest])

                newfloors = floors.copy()
                newfloors[dest] = result
                newfloors[elev] = newfloors[elev].difference(payload)
                nextstates.append((steps + abs(dest - elev), dest, encode(newfloors)))

        for newstate in nextstates:
            # Skip if we've already been here (state + elevator position) in the same or fewer steps
            prior = next(
                (v for v in visited if v[1:] == newstate[1:]),
                None,
            )
            if prior and prior[0] <= newstate[0]:
                continue

            # print(f"  Queueing state {newstate} (take {payload} from {elev} to {dest})")
            heapq.heappush(q, newstate)
            if prior:
                visited.remove(prior)
            visited.append(newstate)

    return 0


# Objective: Get everything to the fourth floor
# Rules:
#  - Elevator must always have 1 or 2 items
#  - A chip cannot be exposed to a foreign generator without its generator
def prob_1(data: list[str]) -> int:
    floors = parse(data)
    return run(floors)


def prob_2(data: list[str]) -> int:
    floors = parse(data)
    max_ltr = sorted(set(i[0] for f in floors for i in f))[-1]
    x, y = chr(ord(max_ltr) + 1), chr(ord(max_ltr) + 2)
    floors[0].update([x + "G", x + "M", y + "G", y + "M"])

    return run(floors)


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2016 day 11.")
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
