"""https://adventofcode.com/2025/day/10"""

from dataclasses import dataclass
from itertools import combinations_with_replacement

from aoclib.runner import solve
from scipy.optimize import linprog

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
    target: list[int]
    buttons: tuple[tuple[int, ...], ...]

    @staticmethod
    def from_line(line: str) -> "JoltageMachine":
        tokens = [v[1:-1] for v in line.split()]  # Trim brackets and parens

        return JoltageMachine(
            list(map(int, tokens[-1].split(","))),
            [tuple(map(int, t.split(","))) for t in tokens[1:-1]],
        )

    def sync_joltage(self) -> int:
        # Apparently this is a linear programming problem. Feels dirty using a prepackaged solver though.
        # TODO: Write a simple solver (e.g. simplex)

        # For each constraint j: 1 if button i includes j else 0
        constraints = [
            [1 if j in b else 0 for b in self.buttons] for j in range(len(self.target))
        ]

        return int(
            round(
                linprog(
                    [1] * len(self.buttons),
                    A_eq=constraints,
                    b_eq=self.target,
                    bounds=[(0, None) for i in range(len(self.buttons))],
                    integrality=[1 for i in range(len(self.buttons))],
                    method="highs",
                ).fun
            )
        )


def prob_1(data: list[str]) -> int:
    return sum(m.sync_lights() for m in [LightMachine.from_line(line) for line in data])


def prob_2(data: list[str]) -> int:
    return sum(
        m.sync_joltage() for m in [JoltageMachine.from_line(line) for line in data]
    )


def main() -> float:
    return solve(__file__, PART, INPUT, prob_1, prob_2)


if __name__ == "__main__":
    main()
