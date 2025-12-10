"""https://adventofcode.com/2025/day/10"""

from dataclasses import dataclass
from itertools import chain, combinations, combinations_with_replacement

from aoclib.runner import solve

# Input file path (or pass with -i <path>)
INPUT = "input.txt"

# Part to solve, 1 or 2 (or pass with -p <1|2|all>)
PART = 1


@dataclass
class LightMachine:
    target: int  # lights target as bitfield
    buttons: tuple[int]  # buttons as bitmasks

    @staticmethod
    def from_line(line: str) -> "LightMachine":
        tokens = [v[1:-1] for v in line.split()]  # Trim brackets and parens
        num_lights = len(tokens[0])
        return LightMachine(
            int("".join("1" if c == "#" else "0" for c in tokens[0]), base=2),
            tuple(
                sum(1 << (num_lights - 1 - int(i)) for i in t.split(","))
                for t in tokens[1:-1]
            ),
        )

    def sync_lights(self) -> int:
        # Try all combinations of X buttons at a time
        # Button press order doesn't matter, so make sure we don't try repeat combos (e.g. 2,0,3,1 vs 0,1,2,3)!
        num_presses = 1
        while True:
            for seq in combinations_with_replacement(self.buttons, num_presses):
                lights = 0
                for b in seq:
                    lights ^= b
                if lights == self.target:
                    return num_presses
            num_presses += 1


@dataclass
class JoltageMachine:
    num_lights: int
    target: list[int]
    buttons: tuple[tuple[int, ...], ...]

    @staticmethod
    def from_line(line: str) -> "JoltageMachine":
        tokens = [v[1:-1] for v in line.split()]  # Trim brackets and parens
        num_lights = len(tokens[0])

        return JoltageMachine(
            num_lights,
            list(map(int, tokens[-1].split(","))),
            [
                tuple(
                    1 if i in map(int, t.split(",")) else 0 for i in range(num_lights)
                )
                for t in tokens[1:-1]
            ],
        )

    def sync_joltage(self) -> int:
        ##
        ## TODO: This is all fucked
        ##
        # We know that there are limits on how many times a button can be pressed...
        # ex. for {3,5,4,7}, we need at least 7 button presses, and we can't press any button that increments
        # the first joltage more than 3 times.
        # So maybe form lower and upper bounds on the number of presses for each button, and form combos from that?
        #
        # Do we want to favor buttons that increment more lights? To get us to the target faster?

        max_presses_per_button = {
            b: min(self.target[i] for i in range(len(self.target)) if b[i] == 1)
            for b in self.buttons
        }

        sorted_buttons = sorted(self.buttons, key=lambda b: sum(b), reverse=True)

        # Make a 'bag' of buttons that can be pressed in any order, up to the upper bound on presses per button
        bag = list(
            chain.from_iterable([b] * max_presses_per_button[b] for b in sorted_buttons)
        )

        num_presses = max(self.target)
        while True:
            for seq in combinations(bag, num_presses):
                joltage = [sum(b[i] for b in seq) for i in range(self.num_lights)]
                if joltage == self.target:
                    return num_presses
            num_presses += 1


def prob_1(data: list[str]) -> int:
    return sum(m.sync_lights() for m in [LightMachine.from_line(line) for line in data])


def prob_2(data: list[str]) -> int:
    machines = [JoltageMachine.from_line(line) for line in data]

    for m in machines[:1]:
        print(m.sync_joltage())

    return 0


if __name__ == "__main__":
    solve(__file__, PART, INPUT, prob_1, prob_2)
