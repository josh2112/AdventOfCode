import argparse
import datetime
import sys
from concurrent import interpreters
from pathlib import Path


def run(path: Path) -> float:
    sys.path.append(str(path))
    sys.argv += ["-p", "all", "-i", "input.txt"]
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

    for day in range(1, max_day + 1):
        if day == 10:
            # TODO: This crashes out pretty good. Is it because day 10 pulls in scipy.optimize?
            print("(skipping day 10)")
            continue
        try:
            print("==============")
            print(f"Year {args.year} day {day}")
            interp = interpreters.create()
            elapsed += interp.call(run, p / str(day))
        except Exception as ex:
            raise RuntimeError(
                f"Failed to run day {day}. Does it have a main() function? Does it have input.txt?"
            ) from ex
        finally:
            interp.close()

    print("==============")
    print(f"Total time: {elapsed}")
