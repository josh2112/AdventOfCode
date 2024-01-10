"""Runs all AoC 2023 solvers, both parts, and prints total time"""

import os
import sys


# Go into each daily directory, import and run the solve script with "-p all" to do both parts.
def main():
    total_time = 0.0
    base = os.getcwd()

    sys.argv.extend(("-p", "all"))

    # These need work!
    skip = (5, 17, 18, 21, 25)

    for day in [d for d in range(1, 26) if d not in skip]:
        print(f"--------[ Day {day} ]--------")

        os.chdir(os.path.join(base, str(day)))
        script = __import__(f"{day}.solve")
        total_time += script.solve.main()

    print(f"--------[ Total time: {total_time} s ]--------")


if __name__ == "__main__":
    main()
