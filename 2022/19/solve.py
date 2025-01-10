"""https://adventofcode.com/2022/day/19"""

import argparse
import math
import re
import time
from dataclasses import dataclass, field

# Input file path (default is "input.txt")
INPUT = "input.txt"

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
    max_ore_cost: int = field(init=False)

    def __post_init__(self):
        self.max_ore_cost = max(
            self.orebot_ore_cost,
            self.claybot_ore_cost,
            self.obsbot_ore_cost,
            self.geobot_ore_cost,
        )


def parse(data: list[str]) -> list[Blueprint]:
    return [Blueprint(*[int(v) for v in re.findall(r"(\d+)", line)]) for line in data]


def run(b: Blueprint, time_rem: int, bots: list[int], res: list[int]):
    # For each of the 4 robot types, figure out how long until we can build
    # another one. If we have time, do it.
    # Ex: clay robot costs 5 ore. We have 2 ore and 2 ore robots, so we need 3 more ore, which will take
    # the 2 robots ceil(3/2) = 2 seconds to produce.

    def project_resources(elapsed: int, costs: list[int]) -> list[int]:
        # Calculate resources after 'elapsed' seconds and spending 'costs'"
        return [r + b * elapsed - c for r, b, c in zip(res, bots, costs)]

    def project_time_to_next_bot(cost, inv, num_bots):
        if inv >= cost:
            return 0
        else:
            return max(math.ceil((cost - inv) / num_bots), -1)

    # Calculate time until we can build, setting to -1 if we don't have
    # any bots of a certain type we need, or we already have enough bots of that type.
    next_bot_times = [
        # Ore
        project_time_to_next_bot(b.orebot_ore_cost, res[ORE], bots[ORE])
        if bots[ORE] < b.max_ore_cost
        else -1,
        # Clay
        project_time_to_next_bot(b.claybot_ore_cost, res[ORE], bots[ORE])
        if bots[CLAY] < b.obsbot_clay_cost
        else -1,
        # Obsidian
        max(
            project_time_to_next_bot(b.obsbot_ore_cost, res[ORE], bots[ORE]),
            project_time_to_next_bot(b.obsbot_clay_cost, res[CLAY], bots[CLAY]),
        )
        if bots[CLAY] and bots[OBS] < b.geobot_obs_cost
        else -1,
        # Geode
        max(
            project_time_to_next_bot(b.geobot_ore_cost, res[ORE], bots[ORE]),
            project_time_to_next_bot(b.geobot_obs_cost, res[OBS], bots[OBS]),
        )
        if bots[OBS]
        else -1,
    ]

    # Add one minute to actually build the bot, and cancel if we don't have time
    next_bot_times = [n + 1 if 0 <= n < time_rem - 1 else None for n in next_bot_times]

    # Don't build any more ore bots 2 seconds from the end
    if next_bot_times[ORE] and next_bot_times[ORE] > time_rem - 2:
        next_bot_times[ORE] = None

    if not any(next_bot_times):
        # No more robots can be built? Project & return geode count at t=0
        return res[GEO] + bots[GEO] * time_rem

    # Return max geodes we could generate by building any possible robot (or none)
    return max(
        res[GEO],
        # Geode
        run(
            b,
            time_rem - next_bot_times[GEO],
            [b + n for b, n in zip(bots, [0, 0, 0, 1])],
            project_resources(
                next_bot_times[GEO], [b.geobot_ore_cost, 0, b.geobot_obs_cost, 0]
            ),
        )
        if next_bot_times[GEO]
        else 0,
        # Obsidian
        run(
            b,
            time_rem - next_bot_times[OBS],
            [b + n for b, n in zip(bots, [0, 0, 1, 0])],
            project_resources(
                next_bot_times[OBS], [b.obsbot_ore_cost, b.obsbot_clay_cost, 0, 0]
            ),
        )
        if next_bot_times[OBS]
        else 0,
        # Clay
        run(
            b,
            time_rem - next_bot_times[CLAY],
            [b + n for b, n in zip(bots, [0, 1, 0, 0])],
            project_resources(next_bot_times[CLAY], [b.claybot_ore_cost, 0, 0, 0]),
        )
        if next_bot_times[CLAY]
        else 0,
        # Ore
        run(
            b,
            time_rem - next_bot_times[ORE],
            [b + n for b, n in zip(bots, [1, 0, 0, 0])],
            project_resources(next_bot_times[ORE], [b.orebot_ore_cost, 0, 0, 0]),
        )
        if next_bot_times[ORE]
        else 0,
    )


def geode_count(b: Blueprint, total_time: int) -> int:
    geodes = run(b, total_time, bots=[1, 0, 0, 0], res=[0, 0, 0, 0])
    print(f"Blueprint {b.id}: {geodes} geodes")
    return geodes


def prob_1(data: list[str]) -> int:
    return sum(b.id * geode_count(b, 24) for b in parse(data))


def prob_2(data: list[str]) -> int:
    # TODO: This takes over 13 minutes. Can we do better?
    return math.prod(geode_count(b, 32) for b in parse(data)[:3])


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
