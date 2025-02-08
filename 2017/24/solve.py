"""https://adventofcode.com/2017/day/24"""

from aoclib.runner import solve
import heapq
from dataclasses import dataclass, field

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


@dataclass(frozen=True, order=True)
class Pipe:
    a: int = field(compare=False)
    b: int = field(compare=False)
    sorted: tuple[int, int]

    @classmethod
    def make(cls, a: int, b: int) -> "Pipe":
        return Pipe(a, b, tuple(sorted((a, b))))


def dfs(pipes: set[Pipe]) -> int:
    def _dfs(b: list[Pipe]):
        conn = b[-1].b
        frontier = [p for p in pipes - set(b) if conn == p.a or conn == p.b]
        return (
            max(
                _dfs(b + [Pipe.make(p.b, p.a) if p.b == b[-1].b else p])
                for p in frontier
            )
            if frontier
            else sum(p.a + p.b for p in b)
        )

    return max(_dfs([p]) for p in pipes if p.a == 0)


def dfs_2(pipes: set[Pipe]) -> int:
    len_longest, score_longest = 0, 0

    def _dfs(b: list[Pipe]):
        conn = b[-1].b
        frontier = [p for p in pipes - set(b) if conn == p.a or conn == p.b]
        for p in frontier:
            _dfs(b + [Pipe.make(p.b, p.a) if p.b == b[-1].b else p])
        if not frontier:
            nonlocal len_longest, score_longest
            if len(b) >= len_longest:
                len_longest = len(b)
                score_longest = max(
                    score_longest if len(b) == len_longest else 0,
                    sum(p.a + p.b for p in b),
                )

    [_dfs([p]) for p in pipes if p.a == 0]
    return score_longest


def prob_1(data: list[str]) -> int:
    return dfs(set(Pipe.make(*map(int, line.split("/"))) for line in data))


def prob_2(data: list[str]) -> int:
    return dfs_2(set(Pipe.make(*map(int, line.split("/"))) for line in data))


if __name__ == "__main__":
    solve(__file__, PART, INPUT, prob_1, prob_2)
