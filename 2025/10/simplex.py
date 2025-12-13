"""
https://www.emathhelp.net/calculators/linear-programming/simplex-method-calculator/?z=a%2Bb%2Bc%2Bd%2Be%2Bf&c=e%2Bf+%3D+3%3B+b%2Bf+%3D+5%3B+c%2Bd%2Be+%3D+4%3B+a%2Bb%2Bd+%3D+7&n=on&m=m

Minimize Z = a+b+c+d+e+f, subject to
e+f = 3,
b+f = 5,
c+d+e = 4,
a+b+d = 7,
all variables >= 0
"""

from fractions import Fraction as F


# Represents each entry in the tableau as (cons + M*coef)
class Entry:
    def __init__(self, cons: F, coef: F):
        self.cons, self.coef = cons, coef

    def __str__(self):
        abscoef = f"{abs(self.coef) if abs(self.coef) > 1 else ''}M"
        if self.cons and self.coef:
            return f"{self.cons}{'-' if self.coef < 0 else '+'}{abscoef}"
        elif self.cons:
            return str(self.cons)
        elif self.coef:
            return f"{'-' if self.coef < 0 else ''}{abscoef}"
        else:
            return "0"

    def __add__(self, other: Entry):
        return Entry(self.cons + other.cons, self.coef + other.coef)

    def __mul__(self, other: Entry | int):
        if other is int:
            return Entry(self.cons * other, self.coef * other)
        # Ex: (2M-1) * 2 = 4M-2
        # Only one can contain M, the other has to be a constant only
        elif self.coef and other.coef:
            raise "Can't multiply two entries with nonero M!"
        elif other.coef:
            return other * self.cons
        # Now other is the constant
        return Entry(self.cons * other.cons, self.coef * other.cons)


def test_entry_to_str():
    assert str(Entry(0, 0)) == "0"
    assert str(Entry(1, 0)) == "1"
    assert str(Entry(-1, 0)) == "-1"
    assert str(Entry(0, 1)) == "M"
    assert str(Entry(0, -1)) == "-M"
    assert str(Entry(1, 1)) == "1+M"
    assert str(Entry(-1, -1)) == "-1-M"
    assert str(Entry(1, -1)) == "1-M"
    assert str(Entry(-1, 1)) == "-1+M"
    assert str(Entry(2, -2)) == "2-2M"
    assert str(Entry(-2, 2)) == "-2+2M"


class Tableau:
    def __init__(self, constraints: list[list[int]], solutions: list[int]):
        self.tableau = [[Entry(c, 0) for c in row] for row in constraints]
        self.tableau.insert(
            0,
            [Entry(-1, 0)] * len(self.tableau[0]) + [Entry(0, -1)] * 2 + [Entry(0, 0)],
        )
        self.tableau[1].extend([Entry(1, 0), Entry(0, 0)])
        self.tableau[2].extend([Entry(0, 0), Entry(1, 0)])
        for r in self.tableau[3:]:
            r.extend([Entry(0, 0), Entry(0, 0)])
        for i, r in enumerate(self.tableau[1:]):
            r.append(Entry(solutions[i], 0))

    def __str__(self):
        return "\n".join(
            "[" + "".join(f"{str(c):>6}" for c in row) + "]" for row in self.tableau
        )

    def add(self, dest: int, src: int, factor: Entry):
        self.tableau[dest] = [
            self.tableau[dest][i] + factor * self.tableau[src][i]
            for i in range(len(self.tableau[dest]))
        ]


tableau = Tableau(
    [
        [0, 0, 0, 0, 1, 1],
        [0, 1, 0, 0, 0, 1],
        [0, 0, 1, 1, 1, 0],
        [1, 1, 0, 1, 0, 0],
    ],
    [3, 5, 4, 7],
)

print("Initial tableau:")
print(tableau)

print("Remove M from Ys:")
tableau.add(0, 1, Entry(0, 1))  # Add row 2 * M to row 1
tableau.add(0, 2, Entry(0, 1))  # Add row 3 * M to row 1
print(tableau)

# Is it really this easy?
print("Add each of the other rows to first row:")
for i in range(3, len(tableau.tableau)):
    tableau.add(0, i, Entry(1, 0))
print(tableau)

# TODO: The rest
