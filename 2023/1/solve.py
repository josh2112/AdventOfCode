#!/usr/bin/env python3

# Input file path, or None for the default, "input.txt"
INPUT = None

# Daily problem to solve, 1 or 2
PROBLEM = 1


def prob_1(data: list[str]):
    return sum(
        int(x[0]) * 10 + int(x[-1])
        for x in [[c for c in ln if str.isdigit(c)] for ln in data]
    )


def prob_2(data: list[str]):
    words = [
        (w, i + 1)
        for i, w in enumerate(
            ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")
        )
    ]

    def find_digit(line: str, i: int):
        return (
            int(line[i])
            if str.isdigit(line[i])
            else next((pr[1] for pr in words if line[i:].startswith(pr[0])), None)
        )

    ans = 0

    # Clue: ordering is important! "twoone" is 2 if at the beginning of a line and 1 if at the end!
    for ln in data:
        for c in range(len(ln)):
            first = find_digit(ln, c)
            if first:
                ans += 10 * first
                break
        for c in range(len(ln) - 1, -1, -1):
            last = find_digit(ln, c)
            if last:
                ans += last
                break
    return ans


def main():
    with open(INPUT or "input.txt", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    print(f"Problem {PROBLEM}")
    print(prob_1(data) if PROBLEM == 1 else prob_2(data))


if __name__ == "__main__":
    main()
