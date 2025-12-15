"""
Second try.

https://www.pmcalculators.com/simplex-method-calculator/


This one might be a better method?
https://www.zweigmedia.com/simplex/simplex.php?lang=en
Bigger matrix but simpler steps

"""

from fractions import Fraction as F
from math import inf


class Tableau:
    def __init__(self, constraints: [list[list[int]]], solutions: list[int]):
        # Add artificial variables x num constraints
        avs = [[0] * len(constraints) for _ in range(len(constraints))]
        for i in range(len(avs)):
            avs[i][i] = -1
        self.m = [
            constraints[i] + avs[i] + [solutions[i]] for i in range(len(constraints))
        ]
        self.m = [[F(e) for e in row] for row in self.m]

    def __str__(self):
        return "\n".join("[" + "".join(f"{e:>5}" for e in row) + "]" for row in self.m)

    def is_optimal(self):
        return all(e >= 0 for e in self.m[-1])

    def iterate(self):
        piv_col = self.m[-1].index(min(self.m[-1]))
        print(f"Pivot column: {piv_col}")

        ratios = [
            self.m[r][-1] / self.m[r][piv_col] if self.m[r][piv_col] != 0 else inf
            for r in range(len(self.m) - 1)
        ]
        print(f"Ratios: {ratios}")

        pivot_row = ratios.index(min(r for r in ratios if r > 0))
        print(f"Pivot row: {pivot_row}")

        self.m[pivot_row] = [e / self.m[pivot_row][piv_col] for e in self.m[pivot_row]]

        for r in range(len(self.m)):
            for c in range(len(self.m[r])):
                if r != pivot_row and c != piv_col:
                    self.m[r][c] -= self.m[r][piv_col] * self.m[pivot_row][c]

        for r in range(len(self.m)):
            if r != pivot_row:
                self.m[r][piv_col] = 0

        print(f"Optimized:\n{self}")


if __name__ == "__main__":
    tableau = Tableau(
        [
            [0, 0, 0, 0, 1, 1],
            [0, 1, 0, 0, 0, 1],
            [0, 0, 1, 1, 1, 0],
            [1, 1, 0, 1, 0, 0],
            [-1, -1, -1, -1, -1, -1],
        ],
        [3, 5, 4, 7, 0],
    )
    """ tableau = Tableau(
        [
            [1, 3, 2],
            [1, 5, 1],
            [-8.0, -10, -7],
        ],
        [10, 8, 0],
    ) """
    print(f"Initial tableau:\n{tableau}")

    while not tableau.is_optimal():
        tableau.iterate()
