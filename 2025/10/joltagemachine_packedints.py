from dataclasses import dataclass
from itertools import combinations_with_replacement


@dataclass
class JoltageMachine:
    num_lights: int
    precision: int
    target: int  # joltage target and buttons as packed X-precision ints
    max_joltage: int
    buttons: tuple[int]

    @staticmethod
    def from_line(line: str, precision: int) -> "JoltageMachine":
        tokens = [v[1:-1] for v in line.split()]  # Trim brackets and parens
        num_lights = len(tokens[0])
        joltages = list(map(int, tokens[-1].split(",")))

        return JoltageMachine(
            num_lights,
            precision,
            sum(j << (precision * i) for i, j in enumerate(reversed(joltages))),
            max(joltages),
            tuple(
                sum(1 << ((num_lights - 1 - int(i)) * precision) for i in t.split(","))
                for t in tokens[1:-1]
            ),
        )

    def sync_joltage(self) -> int:
        # TODO: Maybe packing joltages into a big int wasn't such a good idea. We need to compare them individually
        # to see if we've gone over everywhere.

        # We know we need at least max(joltages) button presses...

        # We should also know that there are limits on how many times a button can be pressed...
        # ex. for {7,5,12,7,2} we can't press a button that increments 4 more than twice.
        # So maybe form lower and upper bounds on the number of presses for each button, and form combos from that?
        # TODO: All this requires that we go back to list from packed int

        num_presses = self.max_joltage
        while True:
            for seq in combinations_with_replacement(self.buttons, num_presses):
                joltage = sum(seq)
                if joltage == self.target:
                    return num_presses
                if joltage < self.target:
                    print(seq, joltage)
            num_presses += 1
