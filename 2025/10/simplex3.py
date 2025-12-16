"""
I like this method; bigger tableau but steps are much simpler to follow:
https://www.zweigmedia.com/simplex/simplex.php?lang=en
"""

import logging
from fractions import Fraction as F
from math import inf

log = logging.getLogger("simplex")


class Tableau:
    def __init__(
        self, constraints: [list[list[int]]], solutions: list[int], coefs: list[int]
    ):
        self.starred = list(range(len(constraints)))
        # Double rows (I guess '=' constraints need both slack and surplus variables?)
        constraints += constraints + [coefs]
        solutions += solutions + [0]
        # Add artificial variables x num constraints
        avs = [[0] * len(constraints) for _ in range(len(constraints))]
        for i in range(len(avs)):
            avs[i][i] = -1 if i < len(avs) // 2 else 1
        # Build initial tableau rows: constraint row + a.v. row + solution
        self.m = [
            constraints[i] + avs[i] + [solutions[i]] for i in range(len(constraints))
        ]
        self.m = [[F(e) for e in row] for row in self.m]

    def __str__(self):
        return "\n".join("[" + "".join(f"{e:>5}" for e in row) + "]" for row in self.m)

    def solve(self):
        log.info(f"\n==[Initial tableau]==\n{self}")
        log.info("\n==[Phase 1]==")
        self.phase1()
        log.info("\n==[Phase 2]==")
        self.phase2()
        # TODO: Check if all vars are integers - if not, choose first one and do branch-and-bound
        # Rerun the solver twice with the first non-integer variable rounded down and up
        return -self.m[-1][-1]

    def phase1(self):
        while self.starred:
            # 1) For any starred rows with 0 on RHS: negate and unstar
            for r in self.starred:
                if self.m[r][-1] == 0:
                    self.m[r] = [-e for e in self.m[r]]
                    self.starred.remove(r)

            if not self.starred:
                break

            # Find first index of max value in first starred row
            row = self.m[self.starred[0]]
            pivot_col = row.index(max(row[:-1]))
            ratios = [
                r[-1] / r[pivot_col] if r[pivot_col] > 0 else inf for r in self.m[:-1]
            ]
            if min(ratios) == inf:
                raise ArithmeticError("No solution (no ratios > 0)")
            pivot_row = ratios.index(
                min(ratios)
            )  # TODO: If multiple mins, randomly choose?
            if pivot_row in self.starred:
                self.starred.remove(pivot_row)
            log.info(f"Pivot row, col = {pivot_row}, {pivot_col}")
            self.pivot(pivot_row, pivot_col)
            log.info(f"After pivot:\n{self}")

    def pivot(self, row: int, col: int):
        pivot = self.m[row][col]
        self.m[row] = [e / pivot for e in self.m[row]]
        for r in range(len(self.m)):
            if r != row:
                factor = self.m[r][col]
                self.m[r] = [
                    self.m[r][c] - factor * self.m[row][c]
                    for c in range(len(self.m[r]))
                ]

    def phase2(self):
        while True:
            pivot_col = self.m[-1].index(min(self.m[-1][:-1]))
            if self.m[-1][pivot_col] >= 0:
                break
            ratios = [
                r[-1] / r[pivot_col] if r[pivot_col] > 0 else inf for r in self.m[:-1]
            ]
            if min(ratios) == inf:
                raise ArithmeticError("No solution (no ratios > 0)")
            pivot_row = ratios.index(
                min(ratios)
            )  # TODO: If multiple mins, randomly choose?
            log.info(f"Pivot row, col = {pivot_row}, {pivot_col}")
            self.pivot(pivot_row, pivot_col)
            log.info(f"After pivot:\n{self}")


def test():
    probs = file_to_probs("input.ex.txt")
    for prob, ans in zip(probs, [10, 12, 11]):
        assert to_tableau(prob).solve() == ans
    print("Tests: ✅")


def file_to_probs(path: str):
    with open(path, "r") as f:
        return [
            [list(map(int, t[1:-1].split(","))) for t in line.split()[1:]]
            for line in f.readlines()
        ]


def to_zweigmedia(prob: list[list[tuple[int, ...]]]):
    """Makes a problem statement that can be plugged in at
    https://www.zweigmedia.com/simplex/simplex.php?lang=en"""
    btns, target = prob[:-1], prob[-1]
    varnames = [chr(ord("a") + i) for i in range(len(btns))]
    return "\n".join(
        [
            f"minimize Z={'+'.join(varnames)} subject to",
            *[
                f"{'+'.join(varnames[b] for b in range(len(btns)) if i in btns[b])}={target[i]}"
                for i in range(len(target))
            ],
            f"integer {','.join(varnames)}",
        ]
    )


def to_tableau(prob: list[list[tuple[int, ...]]]):
    btns, target = prob[:-1], prob[-1]
    return Tableau(
        [[1 if j in b else 0 for b in btns] for j in range(len(target))],
        target,
        [1] * len(btns),
    )


if __name__ == "__main__":
    # test()
    prob = file_to_probs("input.txt")[6]
    print(to_zweigmedia(prob))
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")
    print(to_tableau(prob).solve())
