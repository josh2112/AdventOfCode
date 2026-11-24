"""https://adventofcode.com/2018/day/15"""

from dataclasses import dataclass

from aoclib.runner import solve

# Input file path (or pass with -i <path>)
INPUT = "input.txt"

# Part to solve, 1 or 2 (or pass with -p <1|2|all>)
PART = 1


@dataclass(slots=True)
class Cell:
    x: int
    y: int

    def __str__(self) -> str:
        return f"{self.x},{self.y}"

    def __lt__(self, other: Cell) -> bool:
        return (self.y, self.x) < (other.y, other.x)

    def dist(self, other: Cell) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


@dataclass(slots=True)
class Unit(Cell):
    ap: int
    hp: int


def prob_1(data: list[str]) -> int:
    spaces = [Cell(x, y) for y, row in enumerate(data) for x, c in enumerate(row) if c != "#"]
    goblins = [Unit(cell.x, cell.y, 3, 200) for cell in spaces if data[cell.y][cell.x] == "G"]
    elves = [Unit(cell.x, cell.y, 3, 200) for cell in spaces if data[cell.y][cell.x] == "E"]

    while True:
        units = sorted([*goblins, *elves])

        for u in units:
            is_elf = u in elves

            # Killed by a previous unit in this turn?
            if not is_elf and u not in goblins:
                continue

            # One side all eliminated?
            if not goblins or not elves:
                return 0  # TODO: Score

            enemies_adj = [enemy for enemy in (goblins if is_elf else elves) if u.dist(enemy) == 1]

            # Not adjacent to an enemy?
            if not enemies_adj:
                pass

    return 0


def prob_2(data: list[str]) -> int:
    print(data)
    return 0


if __name__ == "__main__":
    solve(__file__, PART, INPUT, prob_1, prob_2)
