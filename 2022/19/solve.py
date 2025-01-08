"""https://adventofcode.com/2022/day/19"""

import argparse
import time
import re
import math
from dataclasses import dataclass

# Input file path (default is "input.txt")
INPUT = "input-sample.txt"

# Part to solve, 1 or 2
PART = 1

ORE, CLAY, OBS, GEO = 0, 1, 2, 3


@dataclass
class Blueprint:
    id: int
    orebot_ore_cost: int
    claybot_ore_cost: int
    obsbot_ore_cost: int
    obsbot_clay_cost: int
    geobot_ore_cost: int
    geobot_obs_cost: int


def parse(data: list[str]) -> list[Blueprint]:
    return [Blueprint(*[int(v) for v in re.findall(r"(\d+)", line)]) for line in data]


best_geode_count_at_time = dict()


def run(b: Blueprint, t: int, bots: list[int], res: list[int]):
    # For each of the 4 robot types, figure out how long until we can build
    # another one. If we have time, do it.
    # Ex: clay robot costs 5 ore. We have 1 ore and 2 ore robots. We need 4 ore, so 4/2 = 2 seconds.

    def project_resources(time: int, costs: list[int]) -> list[int]:
        """Returns what resources we would have after 'time' seconds and spending 'costs'"""
        return [r + b * time - c for r, b, c in zip(res, bots, costs)]

    # Calculate time until we can build (plus 1 second to build)
    next_bot_times = [
        max(math.ceil((b.orebot_ore_cost - res[ORE]) / bots[ORE]), 0) + 1,
        max(math.ceil((b.claybot_ore_cost - res[ORE]) / bots[ORE]), 0) + 1,
        (
            max(
                max(math.ceil((b.obsbot_ore_cost - res[ORE]) / bots[ORE]), 0),
                max(math.ceil((b.obsbot_clay_cost - res[CLAY]) / bots[CLAY]), 0),
            )
            + 1
        )
        if bots[CLAY]
        else None,
        (
            max(
                max(math.ceil((b.geobot_ore_cost - res[ORE]) / bots[ORE]), 0),
                max(math.ceil((b.geobot_obs_cost - res[OBS]) / bots[OBS]), 0),
            )
            + 1
        )
        if bots[OBS]
        else None,
    ]
    next_bot_times = [n if n and n < t - 1 else None for n in next_bot_times]

    # print(f"{' ' * (24 - t)} t={t}: times to next bot: {next_bot_times}")

    if all(not n for n in next_bot_times):
        # No more robots can be built? Project & return geode count at t=0
        return res[GEO] + bots[GEO] * t

    if res[GEO] > 1:
        print("geodes: ", res[GEO])

    potential_geo = res[GEO]

    potential_geo = max(
        potential_geo,
        run(
            b,
            t - next_bot_times[0],
            [b + n for b, n in zip(bots, [1, 0, 0, 0])],
            project_resources(next_bot_times[0], [b.orebot_ore_cost, 0, 0, 0]),
        )
        if next_bot_times[0]
        else 0,
    )

    potential_geo = max(
        potential_geo,
        run(
            b,
            t - next_bot_times[1],
            [b + n for b, n in zip(bots, [0, 1, 0, 0])],
            project_resources(next_bot_times[1], [b.claybot_ore_cost, 0, 0, 0]),
        )
        if next_bot_times[1]
        else 0,
    )

    potential_geo = max(
        potential_geo,
        run(
            b,
            t - next_bot_times[2],
            [b + n for b, n in zip(bots, [0, 0, 1, 0])],
            project_resources(
                next_bot_times[2], [b.obsbot_ore_cost, b.obsbot_clay_cost, 0, 0]
            ),
        )
        if next_bot_times[2]
        else 0,
    )

    potential_geo = max(
        potential_geo,
        run(
            b,
            t - next_bot_times[3],
            [b + n for b, n in zip(bots, [0, 0, 0, 1])],
            project_resources(
                next_bot_times[3], [b.geobot_ore_cost, 0, b.geobot_obs_cost, 0]
            ),
        )
        if next_bot_times[3]
        else 0,
    )

    return potential_geo


def geode_count(b: Blueprint, time: int) -> int:
    bots = [1, 0, 0, 0]  # ore, clay, obsidian, geode robot counts
    res = [0, 0, 0, 0]  # ore, clay, obsidian, geode counts
    ans = run(b, time, bots, res)
    return ans


def prob_1(data: list[str]) -> int:
    return sum(b.id * geode_count(b, 24) for b in parse(data))


def prob_2(data: list[str]) -> int:
    print(data)
    return 0


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2022 day 19.")
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
