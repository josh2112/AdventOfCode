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

    def __repr__(self) -> str:
        return f"({self.x},{self.y})"

    def __lt__(self, other: Cell) -> bool:
        return (self.y, self.x) < (other.y, other.x)

    def dist(self, other: Cell) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def adjacent(self) -> set[Cell]:
        return set(
            [Cell(self.x, self.y - 1), Cell(self.x + 1, self.y), Cell(self.x, self.y + 1), Cell(self.x - 1, self.y)]
        )


@dataclass(slots=True)
class Unit:
    cell: Cell
    ap: int
    hp: int

    def __repr__(self) -> str:
        return f"({self.cell.x},{self.cell.y})->{self.hp}"

    def __lt__(self, other: Unit) -> bool:
        return self.cell < other.cell


# BFS from c outward, stopping after the iteration in which we reach any of the
# destination cells
def find_best_reachable_cell(c: Cell, dests: set[Cell], spaces: list[Cell]) -> tuple[Cell | None, int]:
    if c in dests:
        return c, 0

    def bfs(frontier: set[Cell], depth: int, visited: list[Cell]) -> tuple[Cell | None, int]:
        frontier = {c for f in frontier for c in f.adjacent() if c not in visited and c in spaces}
        if not frontier:
            return None, -1
        visited.extend(frontier)
        if (candidates := dests.intersection(frontier)) and candidates:
            return sorted(candidates)[0], depth
        return bfs(frontier, depth + 1, visited)

    frontier = {c}
    depth = 0
    visited = [c]
    return bfs(frontier, depth + 1, visited)


def prob_1(data: list[str]) -> int:
    cells = [Cell(x, y) for y, row in enumerate(data) for x, c in enumerate(row) if c != "#"]
    goblins = [Unit(cell, 3, 200) for cell in cells if data[cell.y][cell.x] == "G"]
    elves = [Unit(cell, 3, 200) for cell in cells if data[cell.y][cell.x] == "E"]

    turn_no = 0

    while True:
        turn_no += 1
        # print("===========================")
        # print("TURN", turn_no)

        units = sorted(chain(goblins, elves))

        for u in units:
            # One side all eliminated?
            if not goblins or not elves:
                # Return final score: number of full rounds * sum of all hit points
                return (turn_no - 1) * sum(u.hp for u in units if u.hp > 0)

            # Killed by a previous unit in this turn?
            if u not in elves and u not in goblins:
                continue

            is_elf = u in elves
            # print(f" UNIT {'elf' if is_elf else 'goblin'} {u}")

            enemies = goblins if is_elf else elves

            spaces = [c for c in cells if c not in [u.cell for u in chain(goblins, elves)]]

            all_enemy_adj = {c for enemy in enemies for c in enemy.cell.adjacent()}

            # MOVE
            if u.cell in all_enemy_adj:
                pass  # print(" ALREADY IN RANGE")
            else:
                # All empty enemy-adjacent cells
                all_free_enemy_adj_cells = {c for c in all_enemy_adj if c in spaces}

                # Determine which ones are reachable
                target, dist = find_best_reachable_cell(u.cell, all_free_enemy_adj_cells, spaces)
                if target:
                    # print(f" Best move is towards {target} ({dist} away)")
                    # If not already there, find first step on best path towards it
                    if dist > 0:
                        target, dist = find_best_reachable_cell(target, u.cell.adjacent(), spaces)
                        # print(f" Best move towards target is {target}")
                    # Do the move
                    assert target
                    u.cell = target
                    # print(f" MOVED to {target}")

            # ATTACK
            enemies_in_range = [e for e in enemies if e.cell in u.cell.adjacent()]
            if not enemies_in_range:
                pass  # print(" NO ENEMY in range to attack")
            if enemies_in_range:
                # print(f" Enemies to attack at {sorted(enemies_in_range)}")
                min_hp = min(e.hp for e in enemies_in_range)
                enemy = sorted(e for e in enemies_in_range if e.hp == min_hp)[0]
                enemy.hp -= u.ap
                # print(f" ATTACK enemy {enemy.cell} -> {enemy.hp} hp")
                if enemy.hp <= 0:
                    # TODO: Does this also remove it from elves/goblins??
                    # print(" Enemy killed")
                    enemies.remove(enemy)

        if (turn_no % 10) == 0:
            print(f" END turn {turn_no}. Goblins at {sorted(g for g in goblins)}, elves at {sorted(e for e in elves)}")

    return 0


# For part 2: Binary search? Start with bounds [3,100]. Alter part_1()
# return immediately when 1 elf dies (too weak) or all goblins are dead (too powerful)
def prob_2(data: list[str]) -> int:
    print(data)
    return 0


if __name__ == "__main__":
    solve(__file__, PART, INPUT, prob_1, prob_2)
