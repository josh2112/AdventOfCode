"""https://adventofcode.com/2023/day/1"""

# Input file path, or None for the default, "input.txt"
import argparse
import time


INPUT = "input.txt"

# Daily problem to solve, 1 or 2
PART = 1


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

    # Clue: ordering is important! "twone" is 2 if at the beginning of a line and 1 if at the end!
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


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2023 day 1.")
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
