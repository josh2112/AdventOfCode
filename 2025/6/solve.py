"""https://adventofcode.com/2025/day/6"""

from operator import add, mul

from aoclib.runner import solve

# Input file path (or pass with -i <path>)
INPUT = "input.txt"

# Part to solve, 1 or 2 (or pass with -p <1|2|all>)
PART = 1


def prob_1(data: list[str]) -> int:
    problems = [line.split() for line in data]

    total = 0
    for i in range(len(problems[0])):
        op = add if problems[-1][i] == "+" else mul
        result = 0 if op == add else 1
        [result := op(result, int(values[i])) for values in problems[:-1]]
        total += result
    return total


def prob_2(data: list[str]) -> int:
    # Build ranges for each column
    indices = [i for i, op in enumerate(data[-1]) if op != " "]
    ranges = [
        range(indices[i], indices[i + 1] - 1) for i in range(len(indices) - 1)
    ] + [range(indices[-1], max(len(line) for line in data))]

    total = 0
    for r in ranges:
        op = add if data[-1][r.start] == "+" else mul
        result = 0 if op == add else 1
        [
            result := op(result, v)
            for v in (int("".join(line[i] for line in data[:-1])) for i in r)
        ]
        total += result
    return total


def main() -> float:
    return solve(__file__, PART, INPUT, prob_1, prob_2, no_strip_input=True)


if __name__ == "__main__":
    main()
