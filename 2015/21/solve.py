"""https://adventofcode.com/2015/day/21"""

import argparse
import time
from collections import namedtuple
from dataclasses import dataclass
from itertools import chain, permutations
from math import ceil
from sys import maxsize

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1

Item = namedtuple("Item", ["cost", "damage", "armor"])

WEAPONS = [
    Item(8, 4, 0),
    Item(10, 5, 0),
    Item(25, 6, 0),
    Item(40, 7, 0),
    Item(74, 8, 0),
]
ARMOR = [
    Item(0, 0, 0),  # armor not required
    Item(13, 0, 1),
    Item(31, 0, 2),
    Item(53, 0, 3),
    Item(75, 0, 4),
    Item(102, 0, 5),
]
RINGS = [
    Item(25, 1, 0),
    Item(50, 2, 0),
    Item(100, 3, 0),
    Item(20, 0, 1),
    Item(40, 0, 2),
    Item(80, 0, 3),
]


@dataclass
class Character:
    hp: int
    damage: int
    armor: int


def battle(p_hp, p_dmg, p_arm, boss_hp, boss_dmg, boss_arm, lose: bool = False) -> bool:
    """Do battle, return true if player wins"""
    p_dmg_per_turn = max(1, p_dmg - boss_arm)
    boss_dmg_per_turn = max(1, boss_dmg - p_arm)
    p_turns_to_defeat = ceil(boss_hp / p_dmg_per_turn)
    boss_turns_to_defeat = ceil(p_hp / boss_dmg_per_turn)
    return (not lose and p_turns_to_defeat <= boss_turns_to_defeat) or (
        lose and p_turns_to_defeat > boss_turns_to_defeat
    )


def prob_1(data: list[str]) -> int:
    boss_hp, boss_dmg, boss_arm = [int(line.split()[-1]) for line in data]
    ring_configs = sorted(
        chain([()], permutations(RINGS, 1), permutations(RINGS, 2)),
        key=lambda rc: sum(r.cost for r in rc),
    )
    sorted_armor = sorted(ARMOR, key=lambda a: a.cost)

    min_cost = maxsize

    for w in sorted(WEAPONS, key=lambda w: w.cost):
        for a in sorted_armor:
            for rc in ring_configs:
                if battle(
                    100,
                    w.damage + sum(r.damage for r in rc),
                    a.armor + sum(r.armor for r in rc),
                    boss_hp,
                    boss_dmg,
                    boss_arm,
                ):
                    cost = w.cost + a.cost + sum(r.cost for r in rc)
                    if cost < min_cost:
                        print(f"Won with cost {cost}")
                        min_cost = cost
    return min_cost


def prob_2(data: list[str]) -> int:
    boss_hp, boss_dmg, boss_arm = [int(line.split()[-1]) for line in data]
    ring_configs = sorted(
        chain([()], permutations(RINGS, 1), permutations(RINGS, 2)),
        key=lambda rc: -sum(r.cost for r in rc),
    )
    sorted_armor = sorted(ARMOR, key=lambda a: -a.cost)

    max_cost = 0

    for w in sorted(WEAPONS, key=lambda w: -w.cost):
        for a in sorted_armor:
            for rc in ring_configs:
                if battle(
                    100,
                    w.damage + sum(r.damage for r in rc),
                    a.armor + sum(r.armor for r in rc),
                    boss_hp,
                    boss_dmg,
                    boss_arm,
                    lose=True,
                ):
                    cost = w.cost + a.cost + sum(r.cost for r in rc)
                    if cost > max_cost:
                        print(f"Lost with cost {cost}")
                        max_cost = cost
    return max_cost


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2015 day 21.")
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
