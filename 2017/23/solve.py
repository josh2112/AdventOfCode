"""https://adventofcode.com/2017/day/23"""

from collections import defaultdict

from aoclib.runner import solve

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 2


def run(prog: list[str], ic: int, regs: dict[str, int], part2: bool = False) -> int:
    def resolve(arg):
        return regs[arg] if str.isalpha(arg[0]) else int(arg)

    num_mul = 0

    while 0 <= ic < len(prog):
        if part2 and ic == 10:  # Optimize 10-23
            b = regs["b"]
            if any(not (b % i) and 2 <= b // i <= b for i in range(2, b + 1)):
                regs["f"] = 0
            ic = 24

        instr, x, y, *_ = prog[ic]

        match instr[2]:
            case "t":  # set
                regs[x] = resolve(y)
            case "b":  # sub
                regs[x] -= resolve(y)
            case "l":  # mul
                regs[x] *= resolve(y)
                num_mul += 1
            case "z":  # jnz
                if resolve(x) != 0:
                    ic += resolve(y) - 1

        ic += 1

    return regs, num_mul


def prob_1(data: list[str]) -> int:
    prog = [(line + " .").split() for line in data]
    regs, num_mul = run(prog, 0, defaultdict(lambda: 0))
    return num_mul


def prob_2(data: list[str]) -> int:
    prog = [(line + " .").split() for line in data]
    regs, num_mul = run(prog, 0, defaultdict(lambda: 0, {"a": 1}), part2=True)
    return regs["h"]


if __name__ == "__main__":
    solve(__file__, PART, INPUT, prob_1, prob_2)
