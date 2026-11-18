"""https://adventofcode.com/2018/day/8"""

from dataclasses import dataclass, field

from aoclib.runner import solve

# Input file path (or pass with -i <path>)
INPUT = "input.txt"

# Part to solve, 1 or 2 (or pass with -p <1|2|all>)
PART = 1


@dataclass
class Node:
    idx: int
    num_children: int
    num_meta: int
    children: list[Node] = field(default_factory=list["Node"])
    meta: list[int] = field(default_factory=list[int])

    def sum(self) -> int:
        if not self.children:
            return sum(self.meta)
        total = 0
        for i in self.meta:
            if i - 1 < self.num_children:
                total += self.children[i - 1].sum()
        return total


def doit(data: list[str], part: int) -> int:
    vals = list(map(int, data[0].split(" ")))
    nodes: list[Node] = []

    def process(i: int) -> tuple[int, Node | None]:
        n = Node(i, vals[i], vals[i + 1])
        nodes.append(n)
        i += 2
        for _ in range(n.num_children):
            i, child = process(i)
            if child:
                n.children.append(child)

        n.meta.extend(vals[i : i + n.num_meta])
        return i + n.num_meta, n

    _, root = process(0)

    if part == 1:
        return sum(m for n in nodes for m in n.meta)
    else:
        assert root
        return root.sum()


if __name__ == "__main__":
    solve(__file__, PART, INPUT, lambda d: doit(d, 1), lambda d: doit(d, 2))
