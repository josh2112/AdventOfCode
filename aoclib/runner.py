import argparse
import os
import shlex
import sys
import time
from pathlib import Path


def solve(solverpath: str, part: str | int, input: str, prob_1, prob_2):
    path = Path(solverpath)
    os.chdir(path.parent)
    year, day = path.parent.parts[-2:]

    parser = argparse.ArgumentParser(description=f"Solves AoC {year} day {day}.")
    parser.add_argument("-p", "--part", choices=("1", "2", "all"), default=str(part))
    parser.add_argument("-i", "--input", default=input)

    # VS Code Python debugger launch config sends your arguments as one big quoted string
    args = parser.parse_args(shlex.split(" ".join(sys.argv[1:])))

    with open(args.input, mode="r", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    start = time.perf_counter()
    if args.part in ("1", "all"):
        print(f"Part 1: {prob_1(data)}")
    if args.part in ("2", "all"):
        print(f"Part 2: {prob_2(data)}")

    print(f"Time: {time.perf_counter() - start} s")
