"""https://adventofcode.com/2018/day/14"""

from collections import deque

from aoclib.runner import solve

# Input file path (or pass with -i <path>)
INPUT = "input.txt"

# Part to solve, 1 or 2 (or pass with -p <1|2|all>)
PART = 1


def doit(data: list[str], part: int) -> str:
    target = [int(data[0])] if part == 1 else list(map(int, data[0]))
    recipes = [3, 7]
    elves = [0, 1]

    candidates: deque[int] = deque()

    while True:
        new_recipes = list(map(int, list(str(recipes[elves[0]] + recipes[elves[1]]))))
        recipes.extend(new_recipes)
        for e, elf in enumerate(elves):
            elves[e] = (elf + recipes[elf] + 1) % len(recipes)
        # print("--------")
        # print(recipes)
        # print(elves)
        if part == 1:
            if len(recipes) > 10 + target[0]:
                return "".join(map(str, recipes[target[0] : target[0] + 10]))
        else:
            # TODO: Need to keep track of each new target[0] we find, then when we
            # have enough digits, check it and either return or discard
            candidates.extend(i + len(recipes) - len(new_recipes) for i, r in enumerate(new_recipes) if r == target[0])
            while (c := candidates[0]) and c + len(target) <= len(recipes):
                if target == recipes[c : len(target) + c]:
                    return c - 1
                candidates.pop()

    return 0


if __name__ == "__main__":
    solve(__file__, PART, INPUT, lambda d: doit(d, 1), lambda d: doit(d, 2))
