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
    def __init__(self, m: F, c: F):
        self.m, self.c = m, c

    def __str__(self):
        if not self.m:
            return str(self.c)
        m = f"{'-' if self.m < 0 else ''}{abs(self.m) if abs(self.m) > 1 else ''}M"
        c = f"{'-' if self.c < 0 else '+'}{abs(self.c)}" if self.c != 0 else ""
        return f"{m}{c}"

    def __add__(self, other: Entry):
        return Entry(self.m + other.m, self.c + other.c)

    def __mul__(self, other: Entry):
        # Only one can contain M, the other has to be a constant only
        if self.m and other.m:
            raise Exception("Can't multiply two entries with nonero M!")
        elif other.m:
            return other * self
        # Now other is the constant
        return Entry(self.m * other.c, self.c * other.c)


def test_entry_to_str():
    assert str(Entry(0, 0)) == "0"
    assert str(Entry(0, 1)) == "1"
    assert str(Entry(0, -1)) == "-1"
    assert str(Entry(1, 0)) == "M"
    assert str(Entry(1, 1)) == "M+1"
    assert str(Entry(1, -1)) == "M-1"
    assert str(Entry(-1, 1)) == "-M+1"
    assert str(Entry(-1, -1)) == "-M-1"
    assert str(Entry(2, -2)) == "2M-2"
    assert str(Entry(-2, 2)) == "-2M+2"


class Tableau:
    def __init__(self, constraints: list[list[int]], solutions: list[int]):
        self.tableau = [[Entry(0, c) for c in row] for row in constraints]
        self.tableau.insert(
            0,
            [Entry(0, -1)] * len(self.tableau[0]) + [Entry(-1, 0)] * 2 + [Entry(0, 0)],
        )
        self.tableau[1].extend([Entry(0, 1), Entry(0, 0)])
        self.tableau[2].extend([Entry(0, 0), Entry(0, 1)])
        for r in self.tableau[3:]:
            r.extend([Entry(0, 0), Entry(0, 0)])
        for i, r in enumerate(self.tableau[1:]):
            r.append(Entry(0, solutions[i]))

    def __str__(self):
        return "\n".join(
            "[" + "".join(f"{str(c):>6}" for c in row) + "]" for row in self.tableau
        )

    def add(self, dest: int, src: int, factor: Entry):
        self.tableau[dest] = [
            self.tableau[dest][i] + factor * self.tableau[src][i]
            for i in range(len(self.tableau[dest]))
        ]


test_entry_to_str()

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
tableau.add(0, 1, Entry(1, 0))  # Add row 2 * M to row 1
tableau.add(0, 2, Entry(1, 0))  # Add row 3 * M to row 1
print(tableau)

# Is it really this easy?
print("Add each of the other rows to first row:")
for i in range(3, len(tableau.tableau)):
    tableau.add(0, i, Entry(0, 1))  # Add row i to row 1
print(tableau)

# TODO: The rest
