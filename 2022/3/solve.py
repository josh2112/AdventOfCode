#!/usr/bin/env python3

# Input file path, or None for the default, "input.txt"
INPUT = None

# Daily problem to solve, 1 or 2
PROBLEM = 1


def prob_1(data: list[str]):
    print(data)


def prob_2(data: list[str]):
    print(data)


def main():
    with open(INPUT or "input.txt", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    print(f"Problem {PROBLEM}")
    print(prob_1(data) if PROBLEM == 1 else prob_2(data))


if __name__ == "__main__":
    main()
