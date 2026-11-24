"""https://adventofcode.com/2018/day/14"""

from aoclib.runner import solve

# Input file path (or pass with -i <path>)
INPUT = "input.txt"

# Part to solve, 1 or 2 (or pass with -p <1|2|all>)
PART = 1


# TODO: This is correct but takes 50 seconds for part 2!
# It takes about 20 seconds to generate the necessary number of recipes and shuffle the elves
# Which means 60% of the time is looking for candidates
# Cut runtime to under 30 seconds with strings
def doit(data: list[str], part: int) -> str:
    target = int(data[0]) if part == 1 else data[0]
    recipes = "37"
    elves = [0, 1]

    # Max 2 entries can be added per round, so for part 2, check len(target)+2-1 from end
    check_window = target + 10 if part == 2 else len(target) + 1

    while True:
        recipes += str(int(recipes[elves[0]]) + int(recipes[elves[1]]))

        for e, elf in enumerate(elves):
            elves[e] = (elf + int(recipes[elf]) + 1) % len(recipes)

        if part == 1:
            if len(recipes) > check_window:
                return recipes[target:check_window]
        elif target in recipes[-check_window:]:
            return recipes.find(target)

    return -1


if __name__ == "__main__":
    solve(__file__, PART, INPUT, lambda d: doit(d, 1), lambda d: doit(d, 2))
