"""https://adventofcode.com/2015/day/22"""

import argparse
import logging
import time
from collections import namedtuple
from dataclasses import dataclass
from enum import Enum
from sys import maxsize

# Input file path (default is "input.txt")
INPUT = "input.txt"

logging.basicConfig(level=logging.WARNING, format="%(message)s")

# Part to solve, 1 or 2
PART = 2

Spell = namedtuple("Spell", ["id", "mana", "damage", "effect_length"])


class Spells(Enum):
    MagicMissile = (53, 4, 0)
    Drain = (73, 2, 0)
    Shield = (113, 0, 6)
    Poison = (173, 3, 6)
    Recharge = (229, 0, 5)

    def __init__(self, mana, dmg, efflen):
        self.mana, self.dmg, self.efflen = mana, dmg, efflen


@dataclass
class Boss:
    hp: int
    dmg: int

    def describe(self):
        logging.info(f"- Boss has {self.hp} hit points")


@dataclass
class Player:
    hp: int
    arm: int
    mana: int
    spent: int = 0

    def describe(self):
        logging.info(
            f"- Player has {self.hp} hit points, {self.arm} armor, {self.mana} mana"
        )


def do_effects(effects: dict[Spell, int], player: Player, boss: Boss):
    for sp in effects:
        effects[sp] = effects[sp] - 1

    if Spells.Shield in effects:
        logging.info(f"Shield's timer is now {effects[Spells.Shield]}.")
    if Spells.Poison in effects:
        boss.hp -= 3
        logging.info(
            f"Poison deals 3 damage; its timer is now {effects[Spells.Poison]}."
        )
    if Spells.Recharge in effects:
        player.mana += 101
        logging.info(
            f"Recharge provides 101 mana; its timer is now {effects[Spells.Recharge]}."
        )

    for sp in list(effects.keys()):
        if effects[sp] == 0:
            logging.info(f"{sp.name} wears off.")
            del effects[sp]
            if sp == Spells.Shield:
                player.arm -= 7


MIN_SPENT = maxsize


@dataclass
class SpellNode:
    parent: "SpellNode | None"
    spell: Spell


def log_win(player: Player, node: SpellNode | None):
    global MIN_SPENT
    logging.warning("*** Boss dead!")
    logging.warning(f" - Total spent: {player.spent}")

    spells = []

    while node:
        spells.insert(0, node.spell.name)
        node = node.parent

    logging.warning(f" - Spells: {spells}")

    MIN_SPENT = min(MIN_SPENT, player.spent)

    return


def do_turn(
    player: Player,
    boss: Boss,
    effects: dict[Spell, int],
    prev_spell_node: SpellNode | None,
    spell: Spell,
    deduct_at_start: bool,
):
    logging.info("\n-- Player turn --")
    player.describe()
    boss.describe()

    if deduct_at_start:
        player.hp -= 1
        if player.hp <= 0:
            logging.info("*** Player dead!")
            return

    do_effects(effects, player, boss)

    if boss.hp <= 0:
        return log_win(player, prev_spell_node)

    logging.info(f"Player casts {spell.name}")
    player.spent += spell.mana
    player.mana -= spell.mana
    if spell.efflen > 0:
        effects[spell] = spell.efflen
    if spell == Spells.Shield:
        player.arm += 7
    elif spell == Spells.MagicMissile:
        logging.info("   ... dealing 4 damage")
        boss.hp -= 4
    elif spell == Spells.Drain:
        logging.info("   ... dealing 2 damage, and healing 2 hit points")
        boss.hp -= 2
        player.hp += 2

    if boss.hp <= 0:
        return log_win(player, prev_spell_node)

    logging.info("\n-- Boss turn --")
    player.describe()
    boss.describe()

    do_effects(effects, player, boss)

    if boss.hp <= 0:
        return log_win(player, prev_spell_node)

    dmg = boss.dmg - player.arm
    logging.info(f"Boss attacks for {dmg} damage!")
    player.hp -= dmg
    if player.hp <= 0:
        logging.info("*** Player dead!")
        return

    global MIN_SPENT

    candidate_spells = [
        s
        for s in Spells
        if s.mana <= player.mana
        # Can play spell if it's in effect with timer = 1!
        # It has its last effect before the player's next turn, then it can immediately be used again
        and (s not in effects or effects[s] == 1)
        and player.spent + s.mana < MIN_SPENT
    ]

    spell_node = SpellNode(prev_spell_node, spell)

    for spell in candidate_spells:
        do_turn(
            Player(player.hp, player.arm, player.mana, player.spent),
            Boss(boss.hp, boss.dmg),
            effects.copy(),
            spell_node,
            spell,
            deduct_at_start,
        )


def play_example(player: Player, boss: Boss, spell_seq: list[Spell]):
    global MIN_SPENT

    effects: dict[Spell, int] = {}

    for s in spell_seq:
        do_turn(player, boss, effects, None, s)

    return MIN_SPENT


def play(player: Player, boss: Boss, deduct_at_start: bool = False) -> int:
    global MIN_SPENT

    effects: dict[Spell, int] = {}

    candidate_spells = [
        s
        for s in Spells
        if s.mana <= player.mana
        and s not in effects
        and player.spent + s.mana < MIN_SPENT
    ]

    for spell in candidate_spells:
        do_turn(
            Player(player.hp, player.arm, player.mana, player.spent),
            Boss(boss.hp, boss.dmg),
            effects.copy(),
            None,
            spell,
            deduct_at_start,
        )

    return MIN_SPENT


def prob_1(data: list[str]) -> int:
    # EXAMPLE 1

    # return play_example(
    #     Player(10, 0, 250), Boss(13, 8), [Spells.Poison, Spells.MagicMissile]
    # )

    # EXAMPLE 2
    # return play_example(
    #     Player(10, 0, 250),
    #     Boss(14, 8),
    #     [
    #         Spells.Recharge,
    #         Spells.Shield,
    #         Spells.Drain,
    #         Spells.Poison,
    #         Spells.MagicMissile,
    #     ],
    # )

    boss_hp, boss_dmg = [int(line.split()[-1]) for line in data]
    return play(Player(50, 0, 500), Boss(boss_hp, boss_dmg))


def prob_2(data: list[str]) -> int:
    boss_hp, boss_dmg = [int(line.split()[-1]) for line in data]
    return play(Player(50, 0, 500), Boss(boss_hp, boss_dmg), deduct_at_start=True)


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2015 day 22.")
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
