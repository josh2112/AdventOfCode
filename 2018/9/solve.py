"""https://adventofcode.com/2018/day/9"""

from dataclasses import dataclass

from aoclib.runner import solve

# Input file path (or pass with -i <path>)
INPUT = "input.txt"

# Part to solve, 1 or 2 (or pass with -p <1|2|all>)
PART = 1


@dataclass(slots=True)
class Marble:
    value: int
    prev: "Marble"
    next: "Marble"


class MarbleCircle:
    def __init__(self):
        self.cur = self.head = Marble(0, None, None) # type: ignore
        self.cur.prev, self.cur.next = self.cur, self.cur

    def move(self, cnt: int):
        for _ in range(abs(cnt)):
            self.cur = self.cur.prev if cnt < 0 else self.cur.next

    def pop(self):
        self.cur.prev.next = self.cur.next
        self.cur.next.prev = self.cur.prev
        val = self.cur.value
        self.cur = self.cur.next
        return val

    def insert(self, val: int):
        m = Marble(val, self.cur.prev, self.cur)
        m.prev.next = m
        m.next.prev = m
        self.cur = m

    def __str__(self) -> str:
        marbles = [self.head]
        m = self.head
        while m.next != self.head:
            m = m.next
            marbles.append(m)
        return " ".join(str(m.value) if m != self.cur else f"({m.value})" for m in marbles)


def prob_1(data: list[str]) -> int:
    words = data[0].split(" ")
    num_players, num_rounds = int(words[0]), int(words[6])
    print(num_players, num_rounds)

    scores = [0 for _ in range(num_players)]

    circle = MarbleCircle()
    cur_player = 0

    for i in range(1, num_rounds + 1):
        # print(f"[{cur_player}] {circle}")

        cur_player = (cur_player + 1) % num_players

        if i % 23:
            circle.move(2)
            circle.insert(i)
        else:
            circle.move(-7)
            scores[cur_player] += i + circle.pop()

    # print(f"[{cur_player}] {circle}")

    return max(scores)


# The circle gets too big if we do 100x more rounds... find some kind of pattern?
def prob_2(data: list[str]) -> int:
    words = data[0].split(" ")
    num_rounds = int(words[6]) * 100
    return prob_1([" ".join([words[0], "a", "a", "a", "a", "a", str(num_rounds)])])


if __name__ == "__main__":
    solve(__file__, PART, INPUT, prob_1, prob_2)
