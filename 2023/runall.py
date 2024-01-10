"""Runs all AoC 2023 solvers, both parts, and prints total time"""

import os
import sys


def main():
    total_time = 0.0
    base = os.getcwd()

    sys.argv.extend(("-p", "all"))

    # These need work!
    skip = (5, 17, 18, 21, 25)

    for d in range(1, 26):
        if d in skip:
            continue
        day = str(d)
        print(f"--------[ Day {day} ]--------")
        os.chdir(os.path.join(base, day))
        script = __import__(f"{day}.solve")

        total_time += script.solve.main()

    print(f"--------[ Total time: {total_time} s ]--------")


if __name__ == "__main__":
    main()
