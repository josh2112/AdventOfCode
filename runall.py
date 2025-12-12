import argparse
import datetime
import sys
from concurrent import interpreters
from pathlib import Path


def run(path: Path) -> float:
    sys.path.append(str(path))
    return __import__("solve").main()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Runs all Advent of Code problems from the specified year"
    )
    parser = argparse.ArgumentParser()
    date = datetime.date.today()
    parser.add_argument("-y", "--year", default=date.year)
    args = parser.parse_args()

    p = Path(str(args.year)).absolute()
    max_day = max([int(d.name) for d in p.iterdir() if d.name.isnumeric()])

    elapsed = 0

    for day in [12, 11]:
        interp = interpreters.create()
        elapsed += interp.call(run, p / str(day))
        interp.close()

    print("==============")
    print(f"Total time: {elapsed}")
