#!/usr/bin/env python3

import argparse
import datetime
import os
from stat import S_IREAD, S_IRGRP, S_IROTH
from string import Template

import requests
from dotenv import load_dotenv

load_dotenv()

AOC_SESSION = os.getenv("AOC_SESSION")
if not AOC_SESSION:
    raise EnvironmentError("Error: AOC_SESSION not found in environment or .env file")


def init_input(year: int, day: int, path: str) -> bool:
    if os.path.exists(path):
        print(f"Warning: {path} already exists, skipping")
        return False

    url = f"https://adventofcode.com/{year}/day/{day}/input"
    headers = {"Cookie": f"session={AOC_SESSION}"}
    r = requests.get(url, headers=headers, timeout=5)

    if r.status_code != 200:
        raise IOError(
            f"Error getting input: HTTP {r.status_code}: {r.reason} \n{r.text}"
        )

    with open(path, mode="w", encoding="utf-8") as f:
        f.write(r.text)
    os.chmod(path, S_IREAD | S_IRGRP | S_IROTH)

    return True


def init_script(year: int, day: int, path: str) -> bool:
    if os.path.exists(path):
        print(f"Warning: {path} already exists, skipping")
        return False

    with open(path, "x", encoding="utf-8") as dest:
        with open("solve.template.py", "r", encoding="utf-8") as src:
            dest.write(Template(src.read()).substitute(year=year, day=day))

    os.chmod(path, 0o744)
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Sets up daily Advent of Code problem",
        epilog="Must supply browser session id in AOC_SESSION env var or in .env file",
    )
    date = datetime.date.today()
    parser.add_argument("-y", "--year", default=date.year)
    parser.add_argument("-d", "--day", default=date.day)
    args = parser.parse_args()
    year = args.year
    day = args.day

    path = os.path.join(str(year), str(day))
    os.makedirs(path, exist_ok=True)

    input_path = os.path.join(path, "input.txt")
    if init_input(year, day, input_path):
        print(f"Wrote input: {input_path}")

    script_path = os.path.join(path, "solve.py")
    if init_script(year, day, script_path):
        print(f"Wrote script: {script_path}")


if __name__ == "__main__":
    main()
