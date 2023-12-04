#!/usr/bin/env python3

# https://adventofcode.com/2023/day/4

# Input file path, or None for the default, "input.txt"
INPUT = "input.txt"

# Daily problem to solve, 1 or 2
PROBLEM = 1


def prob_1(data: list[str]):
    make_list = lambda parts: [[int(d) for d in part.split()] for part in parts]
    rows = [make_list(line.split(":")[1].split("|")) for line in data]
    # return sum(pow(2, len([set(r[0]).intersection(set(r[1])) for r in rows])))
    num_matches = [len(set(r[0]).intersection(set(r[1]))) for r in rows]
    return sum(pow(2, n - 1) if n > 0 else 0 for n in num_matches)
    # return sum(pow(2, len(set(r[0]).intersection(set(r[1]))) - 1) for r in rows)


def prob_2(data: list[str]):
    print(data)


def main():
    with open(INPUT or "input.txt", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    print(f"Problem {PROBLEM}")
    print(prob_1(data) if PROBLEM == 1 else prob_2(data))


if __name__ == "__main__":
    main()
