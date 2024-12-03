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


def parse(data: list[str]):
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
    types, i = {}, 0
    floorcodes = []
    for f in floors:
        for t in f:
            if t[0] not in types:
                types[t[0]] = ascii_uppercase[i]
                i += 1
        floorcodes.append("".join(sorted(types[t[0]] + t[1] for t in f)))
    return ",".join(floorcodes)


def decode(floors):
    return [set(f[i : i + 2] for i in range(0, len(f), 2)) for f in floors.split(",")]


def is_floor_valid(floor) -> bool:
    mc = set(i[0] for i in floor if i[1] == "M")
    gen = set(i[0] for i in floor if i[1] == "G")
    return not gen or not mc.difference(gen)


# Objective: Get everything to the fourth floor
# Rules:
#  - Elevator must always have 1 or 2 items (and 1 must always be a microchip)
#  - A chip cannot be next to a different generator without its corrersponding generator
def prob_1(data: list[str]) -> int:
    floors, elev = parse(data), 0

    init = (0, elev, encode(floors))

    # DEBUG
    # init = (3, 1, "AM,BM,AGBG,")

    q = [init]
    best_state_costs = {q[0][2]: (q[0][0], q[0][1])}

    while q:
        steps, elev, floorcodes = state = heapq.heappop(q)
        print(f"Unqueueing state {state}")
        floors = decode(floorcodes)

        if not floors[0] and not floors[1] and not floors[2]:
            return steps

        # What can the elevator carry from this floor?
        possibs = [(x,) for x in floors[elev]] + list(
            itertools.combinations(floors[elev], 2)
        )
        for pld in possibs:
            # What floors can this payload go to?
            valid_floors = []
            for f in range(elev + 1, 4):
                if is_floor_valid(set(pld).union(floors[f])):
                    valid_floors.append(f)
                else:
                    break
            for f in range(elev - 1, -1, -1):
                if is_floor_valid(set(pld).union(floors[f])):
                    valid_floors.append(f)
                else:
                    break

            for dest in valid_floors:
                result = set(pld).union(floors[dest])

                newfloors = floors.copy()
                newfloors[dest] = result
                newfloors[elev] = newfloors[elev].difference(pld)
                newstate = (steps + abs(dest - elev), dest, encode(newfloors))

                # Skip if we've already been here in the same or fewer steps
                if (
                    newstate[2] in best_state_costs
                    and best_state_costs[newstate[2]][0] <= newstate[0]
                ):
                    continue

                print(f"Queueing state {newstate} (take {pld} from {elev} to {dest})")
                heapq.heappush(q, newstate)
                best_state_costs[newstate[2]] = (newstate[0], newstate[1])

    return 0


def prob_2(data: list[str]) -> int:
    print(data)
    return 0


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
