import argparse
import os
import shlex
import sys
import time
from pathlib import Path
from typing import Callable

Solvefunc = Callable[[list[str]], int]


def _solve(label: str, func: Solvefunc) -> float:
    start = time.perf_counter()
    ans = func()
    elapsed = time.perf_counter() - start
    print(f"Part {label}: {ans}")
    print(f"Time: {elapsed} s")
    return elapsed


def solve(
    solverpath: str,
    part: str | int,
    input: str,
    prob_1: Solvefunc,
    prob_2: Solvefunc,
    no_strip_input: bool = False,
) -> float:
    # no_strip_input: For some problems the leading and trailing whitepsace is
    # important. Set this to true to preserve it (newline will still be stripped).
    path = Path(solverpath)
    os.chdir(path.parent)
    year, day = path.parent.parts[-2:]

    parser = argparse.ArgumentParser(description=f"Solves AoC {year} day {day}.")
    parser.add_argument("-p", "--part", choices=("1", "2", "all"), default=str(part))
    parser.add_argument("-i", "--input", default=input)

    # VS Code Python debugger launch config sends your arguments as one big quoted string
    args = parser.parse_args(shlex.split(" ".join(sys.argv[1:])))

    with open(args.input, mode="r", encoding="utf-8") as f:
        data = [line[:-1] if no_strip_input else line.strip() for line in f.readlines()]

    elapsed = 0

    if args.part in ("1", "all"):
        elapsed += _solve("1", lambda: prob_1(data))
    if args.part in ("2", "all"):
        elapsed += _solve("2", lambda: prob_2(data))

    return elapsed
