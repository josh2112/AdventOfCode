#!/usr/bin/env python3

# https://adventofcode.com/2023/day/4

# Input file path, or None for the default, "input.txt"
INPUT = "input.txt"

# Daily problem to solve, 1 or 2
PROBLEM = 2


class Card:
    def __init__(self, line: str):
        self.count = 1
        part1, part2 = line.split(":")
        self.index = int(part1.split()[1]) - 1
        self.nums1, self.nums2 = [[int(d) for d in part.split()] for part in part2.split("|")]
        self.num_matches = len(set(self.nums1).intersection(set(self.nums2)))


def prob_1(data: list[str]):
    cards = [Card(line) for line in data]
    return sum(pow(2, n - 1) if n > 0 else 0 for n in [c.num_matches for c in cards])


def prob_2(data: list[str]):
    cards = [Card(line) for line in data]
    for c, card in enumerate(cards):
        for i in range(c + 1, c + 1 + card.num_matches):
            cards[i].count += card.count
    return sum(c.count for c in cards)


def main():
    with open(INPUT or "input.txt", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    print(f"Problem {PROBLEM}")
    print(prob_1(data) if PROBLEM == 1 else prob_2(data))


if __name__ == "__main__":
    main()
