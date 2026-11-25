"""https://adventofcode.com/2018/day/15"""

from dataclasses import dataclass
from itertools import chain

from aoclib.runner import solve

# Input file path (or pass with -i <path>)
INPUT = "input.txt"

# Part to solve, 1 or 2 (or pass with -p <1|2|all>)
PART = 1


@dataclass(slots=True, frozen=True)
class Cell:
    x: int
    y: int

    def __str__(self) -> str:
        return f"{self.x},{self.y}"

    def __lt__(self, other: Cell) -> bool:
        return (self.y, self.x) < (other.y, other.x)

    def dist(self, other: Cell) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def adjacent(self) -> list[Cell]:
        return [Cell(self.x, self.y - 1), Cell(self.x + 1, self.y), Cell(self.x, self.y + 1), Cell(self.x - 1, self.y)]


@dataclass(slots=True)
class Unit:
    cell: Cell
    ap: int
    hp: int

    def __lt__(self, other: Unit) -> bool:
        return self.cell < other.cell


# BFS from c outward, stopping after the iteration in which we reach cell(s) from
# all_enemy_adj_cells
def find_best_reachable_cell(c: Cell, all_enemy_adj_cells: set[Cell], spaces: list[Cell]):
    if c in all_enemy_adj_cells:
        return c

    def bfs(frontier: list[Cell], depth: int, visited: list[Cell]) -> Cell | None:
        frontier = [c for f in frontier for c in f.adjacent() if c in spaces and c not in visited]
        if not frontier:
            return None
        visited.extend(frontier)
        if (candidates := all_enemy_adj_cells.intersection(frontier)) and candidates:
            return sorted(candidates)[0]
        return bfs(frontier, depth + 1, visited)

    frontier = [c]
    depth = 0
    visited = [c]
    return bfs(frontier, depth + 1, visited)


def prob_1(data: list[str]) -> int:
    cells = [Cell(x, y) for y, row in enumerate(data) for x, c in enumerate(row) if c != "#"]
    goblins = [Unit(cell, 3, 200) for cell in cells if data[cell.y][cell.x] == "G"]
    elves = [Unit(cell, 3, 200) for cell in cells if data[cell.y][cell.x] == "E"]

    while True:
        units = sorted(chain(goblins, elves))

        for u in units:
            # One side all eliminated?
            if not goblins or not elves:
                return 0  # TODO: Score

            # Killed by a previous unit in this turn?
            if u not in elves and u not in goblins:
                continue

            is_elf = u in elves
            enemies = goblins if is_elf else elves

            spaces = [c for c in cells if c not in [u.cell for u in chain(goblins, elves)]]

            # All empty enemy-adjacent cells
            all_enemy_adj_cells = {c for enemy in enemies for c in enemy.cell.adjacent() if c in spaces}

            # Determine which ones are reachable
            reachable = find_best_reachable_cell(u.cell, all_enemy_adj_cells, spaces)

            print(f"Gonna move {u.cell} to {reachable}")
            return

    return 0


def prob_2(data: list[str]) -> int:
    print(data)
    return 0


if __name__ == "__main__":
    solve(__file__, PART, INPUT, prob_1, prob_2)
