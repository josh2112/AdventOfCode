"""https://adventofcode.com/2018/day/4"""

from collections import defaultdict

from aoclib.runner import solve

# Input file path (or pass with -i <path>)
INPUT = "input.txt"

# Part to solve, 1 or 2 (or pass with -p <1|2|all>)
PART = 1


def parse_input(data: list[str]) -> dict[str, list[range]]:
    guards: dict[str, list[range]] = defaultdict(list)
    g: str | None = None
    f = 0
    for line in sorted(data, key=lambda line: line[6:17]):
        match line[19]:
            case "G":
                g = line[26:].split()[0]
            case "f":
                f = int(line[15:17])
            case "w":
                guards[g].append(range(f, int(line[15:17])))
    return guards


def build_mins_asleep(guard: list[range]) -> list[int]:
    mins_asleep = [0] * 60
    for r in guard:
        for m in r:
            mins_asleep[m] += 1
    return mins_asleep


def prob_1(data: list[str]) -> int:
    guards = parse_input(data)
    sleepiest = max(guards, key=lambda g: sum(len(r) for r in guards[g]))
    mins_asleep = build_mins_asleep(guards[sleepiest])
    return int(sleepiest) * max(enumerate(mins_asleep), key=lambda v: v[1])[0]


def prob_2(data: list[str]) -> int:
    guards = parse_input(data)
    guard, minute, minutes_cnt = None, 0, 0

    for g in guards:
        mins_asleep = build_mins_asleep(guards[g])
        i, v = max(enumerate(mins_asleep), key=lambda v: v[1])
        if v > minutes_cnt:
            guard, minute, minutes_cnt = g, i, v

    return int(guard) * minute


if __name__ == "__main__":
    solve(__file__, PART, INPUT, prob_1, prob_2)
