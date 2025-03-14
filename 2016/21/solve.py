"""https://adventofcode.com/2016/day/21"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def rot(pwd: list[str], cnt: int):
    return pwd[-(cnt % len(pwd)) :] + pwd[: -(cnt % len(pwd))]


def scramble(data: list[str], pwdstr: str):
    pwd = list(pwdstr)
    for line in data:
        tk = line.split()
        if line.startswith("swap p"):
            x, y = int(tk[2]), int(tk[5])
            pwd[x], pwd[y] = pwd[y], pwd[x]
        elif line.startswith("swap"):
            x, y = pwd.index(tk[2]), pwd.index(tk[5])
            pwd[x], pwd[y] = pwd[y], pwd[x]
        elif line.startswith("rotate b"):
            x = pwd.index(tk[6])
            pwd = rot(pwd, x + 1 + (1 if x >= 4 else 0))
        elif line.startswith("rotate"):
            pwd = rot(pwd, int(tk[2]) * (-1 if tk[1].startswith("l") else 1))
        elif line.startswith("rev"):
            x, y = int(tk[2]), int(tk[4])
            pwd = pwd[:x] + list(reversed(pwd[x : y + 1])) + pwd[y + 1 :]
        elif line.startswith("move"):
            x, y = int(tk[2]), int(tk[5])
            pwd.insert(y, pwd.pop(x))
    return "".join(pwd)


def unscramble(data: list[str], pwdstr: str):
    pwd = list(pwdstr)
    for line in reversed(data):
        tk = line.split()
        if line.startswith("swap p"):
            x, y = int(tk[2]), int(tk[5])
            pwd[x], pwd[y] = pwd[y], pwd[x]
        elif line.startswith("swap"):
            x, y = pwd.index(tk[2]), pwd.index(tk[5])
            pwd[x], pwd[y] = pwd[y], pwd[x]
        elif line.startswith("rotate b"):
            x1 = pwd.index(tk[6])
            # Find the original position that would've caused the letter to move here
            x0 = next(
                i
                for i in range(len(pwd))
                if ((2 * i + 1 + (1 if i >= 4 else 0)) % len(pwd)) == x1
            )
            pwd = rot(pwd, (x0 - x1) % -len(pwd))
        elif line.startswith("rotate"):
            pwd = rot(pwd, int(tk[2]) * (1 if tk[1].startswith("l") else -1))
        elif line.startswith("rev"):
            x, y = int(tk[2]), int(tk[4])
            pwd = pwd[:x] + list(reversed(pwd[x : y + 1])) + pwd[y + 1 :]
        elif line.startswith("move"):
            x, y = int(tk[2]), int(tk[5])
            pwd.insert(x, pwd.pop(y))
    return "".join(pwd)


def prob_1(data: list[str]) -> int:
    # return scramble(data, "abcde")
    return scramble(data, "abcdefgh")


def prob_2(data: list[str]) -> int:
    return unscramble(data, "fbgdceah")


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2016 day 21.")
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
