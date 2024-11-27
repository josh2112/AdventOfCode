"""https://adventofcode.com/2016/day/7"""

import argparse
import time
import re

# Input file path (default is "input.txt")
INPUT = "input.ex2.txt"

# Part to solve, 1 or 2
PART = 1


def contains_abba(str: str) -> bool:
    for i in range(3, len(str)):
        if str[i - 3] == str[i] and str[i - 1] == str[i - 2] and str[i] != str[i - 1]:
            return True
    return False


def find_abas(str: str) -> str:
    for i in range(2, len(str)):
        if str[i - 2] == str[i] and str[i - 1] != str[i]:
            yield str[i - 2 : i + 1]


def prob_1(data: list[str]) -> int:
    num_tls = 0
    for line in data:
        good_tls, bad_tls = False, False
        for pair in re.findall(r"(?P<out>\w+)(?P<in>\[\w+\])?", line):
            good_tls |= contains_abba(pair[0])
            bad_tls |= contains_abba(pair[1][1:-1]) if pair[1] else False
        num_tls += 1 if good_tls and not bad_tls else 0
    return num_tls


def prob_2(data: list[str]) -> int:
    num_ssl = 0
    for line in data:
        pairs = re.findall(r"(?P<out>\w+)(?P<in>\[\w+\])?", line)
        abas_g1 = [a for b in [list(find_abas(p[0])) for p in pairs] for a in b]
        abas_g2 = [
            a for b in [list(find_abas(p[1])) for p in pairs if len(p) == 2] for a in b
        ]
        abas_g2 = ["".join((a[1], a[0], a[1])) for a in abas_g2]
        num_ssl += 1 if any(a in abas_g2 for a in abas_g1) else 0
    return num_ssl


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2016 day 7.")
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
