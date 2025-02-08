"""https://adventofcode.com/2017/day/25"""

from aoclib.runner import solve
import re
from dataclasses import dataclass


# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


@dataclass
class Transition:
    write: int
    move: int
    state: int


@dataclass
class State:
    name: str
    x0: Transition
    x1: Transition

    @classmethod
    def make(cls, name, w0, m0, s0, w1, m1, s1):
        return State(
            name,
            Transition(int(w0), 1 if m0 == "right" else -1, s0),
            Transition(int(w1), 1 if m1 == "right" else -1, s1),
        )


@dataclass
class Slot:
    val: int
    prev: "Slot|None"
    next: "Slot|None"


def parse(data: list[str]) -> tuple[str, int, dict[str, State]]:
    data = "\n".join(data).split("\n\n")

    start, steps = re.match(r".*(\w).\n.*after (\d+)", data[0]).groups()
    states = [
        State.make(
            *re.match(
                r".*(\w):\n.*\n.*(\d).\n.*(left|right).\n.*(\w).\n.*\n.*(\d).\n.*(left|right).\n.*(\w).",
                g,
            ).groups()
        )
        for g in data[1:]
    ]

    return start, int(steps), {s.name: s for s in states}


def prob_1(data: list[str]) -> int:
    state, steps, states = parse(data)
    state = states[state]
    slot = head = Slot(0, None, None)

    for i in range(steps):
        xn = state.x0 if slot.val == 0 else state.x1
        slot.val = xn.write
        state = states[xn.state]
        if xn.move == 1:
            if not slot.next:
                slot.next = Slot(0, slot, None)
            slot = slot.next
        else:
            if not slot.prev:
                slot.prev = Slot(0, None, slot)
                head = slot.prev
            slot = slot.prev

    slot = head
    chk = slot.val
    while slot := slot.next:
        chk += slot.val
    return chk


def prob_2(data: list[str]) -> int:
    return "freebie!"


if __name__ == "__main__":
    solve(__file__, PART, INPUT, prob_1, prob_2)
