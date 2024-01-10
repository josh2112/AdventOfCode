"""https://adventofcode.com/2023/day/7"""

import argparse
from dataclasses import dataclass
from enum import IntEnum
from functools import cmp_to_key
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 2

CARDS = [str(i) for i in range(2, 10)] + ["T", "J", "Q", "K", "A"]


class HandType(IntEnum):
    INVALID = 0
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_KIND = 4
    FULL_HOUSE = 5
    FOUR_KIND = 6
    FIVE_KIND = 7


DISTINCT_CARDS_TO_HAND_TYPE = {1: 7, 2: 6, 3: 4, 4: 2, 5: 1}


def cards2str(cards: list[int]):
    return "".join(CARDS[c] for c in cards)


def classify(cards: list[int]) -> HandType:
    cardset = set(cards)
    t = HandType(DISTINCT_CARDS_TO_HAND_TYPE[len(cardset)])
    if len(cardset) == 2 or len(cardset) == 3:
        hist = {}
        for c in cards:
            hist[c] = hist.get(c, 0) + 1
        if len(cardset) == 2:
            # four of a kind or full house?
            t = HandType.FOUR_KIND if 4 in hist.values() else HandType.FULL_HOUSE
        else:
            # three of a kind or two pair?
            t = HandType.THREE_KIND if 3 in hist.values() else HandType.TWO_PAIR
    return t


def classify_with_wildcard(cards: list[int]) -> HandType:
    if 0 not in cards:
        return classify(cards)
    wildcard_indices = [i for i, c in enumerate(cards) if c == 0]
    best_type = HandType.INVALID
    for i in range(len(CARDS) - 1, -1, -1):
        for w in wildcard_indices:
            cards[w] = i
        t = classify(cards)
        if t > best_type:
            best_type = t
    return best_type


@dataclass
class Hand:
    cards: list[int]
    bid: int
    type: HandType

    def __init__(self, line: str):
        (cards, bid) = line.split()
        self.cards = [CARDS.index(c) for c in cards]
        self.bid = int(bid)

        self.type = (
            classify(self.cards) if PART == 1 else classify_with_wildcard(self.cards)
        )


def compare_hands(h1: Hand, h2: Hand) -> int:
    if h1.type < h2.type:
        return -1
    if h1.type > h2.type:
        return 1
    for i, c in enumerate(h1.cards):
        if c < h2.cards[i]:
            return -1
        if c > h2.cards[i]:
            return 1
    return 0


# TODO: Somehow broke part 1 solution when doing part 2...
def prob_1(data: list[str]):
    hands = sorted([Hand(line) for line in data], key=cmp_to_key(compare_hands))
    return sum(h.bid * (i + 1) for (i, h) in enumerate(hands))


def prob_2(data: list[str]):
    CARDS.remove("J")
    CARDS.insert(0, "J")
    hands = sorted([Hand(line) for line in data], key=cmp_to_key(compare_hands))
    return sum(h.bid * (i + 1) for (i, h) in enumerate(hands))


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2023 day 7.")
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
