"""https://adventofcode.com/2017/day/18"""

import argparse
import time
from collections import defaultdict

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def run(prog: list[str], state, part2: bool = False) -> int:
    def resolve(arg):
        return regs[arg] if str.isalpha(arg[0]) else int(arg)

    ic, regs, qrecv, qsend = state
    lastsnd = -1
    num_sent = 0

    while 0 <= ic < len(prog):
        instr, x, y, *_ = prog[ic]

        match instr[1]:
            case "n":  # snd
                if part2:
                    qsend.append(resolve(x))
                    num_sent += 1
                else:
                    lastsnd = resolve(x)
            case "e":  # set
                regs[x] = resolve(y)
            case "d":  # add
                regs[x] += resolve(y)
            case "u":  # mul
                regs[x] *= resolve(y)
            case "o":  # mod
                regs[x] %= resolve(y)
            case "c":  # rcv
                if part2:
                    if qrecv:
                        regs[x] = qrecv.pop(0)
                    else:
                        return (ic, regs, qrecv, qsend), num_sent
                elif resolve(x):
                    return lastsnd
            case "g":  # jgz
                if resolve(x) > 0:
                    ic += resolve(y) - 1

        ic += 1

    return (ic, regs, qrecv, qsend), num_sent


def prob_1(data: list[str]) -> int:
    prog = [(line + " .").split() for line in data]
    return run(prog, (0, defaultdict(lambda: 0), None, None))


def prob_2(data: list[str]) -> int:
    prog = [(line + " .").split() for line in data]

    q0, q1 = [], []

    # IC, regs, recv queue, send queue
    state0 = (0, defaultdict(lambda: 0, {"p": 0}), q0, q1)
    state1 = (0, defaultdict(lambda: 0, {"p": 1}), q1, q0)

    state1_values_sent = 0

    # While either state's IC is valid and either state is not deadlocked...
    while ((0 <= state0[0] < len(prog)) or (0 <= state1[0] < len(prog))) and not (
        (prog[state0[0]][0][1] == "c" and not state0[2])
        and (prog[state1[0]][0][1] == "c" and not state1[2])
    ):
        state0, _ = run(prog, state0, part2=True)
        state1, num_sent1 = run(prog, state1, part2=True)
        state1_values_sent += num_sent1

    return state1_values_sent


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solves AoC 2017 day 18.")
    parser.add_argument("-p", "--part", choices=("1", "2", "all"), default=str(PART))
    parser.add_argument("-i", "--input", default=INPUT)
    args = parser.parse_args()

    with open(args.input, mode="r", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    start = time.perf_counter()
    if args.part in ("1", "all"):
        print(f"Part 1: {prob_1(data)}")
    if args.part in ("2", "all"):
        print(f"Part 2: {prob_2(data)}")

    print(f"Time: {time.perf_counter() - start} s")
