#!/usr/bin/env python3

import dataclasses
import re
import time

# https://adventofcode.com/2023/day/20

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 2


@dataclasses.dataclass
class Module:
    name: str
    targets: list[str]
    symbol: str
    is_on: int = 0
    inputs: dict[str, bool] = dataclasses.field(default_factory=dict)

    @staticmethod
    def parse(line: str):
        m = list(re.finditer(r"([^\s\->,])+", line))
        name, symbol = m[0][0], ""
        if not name[0].isalpha():
            symbol = name[0]
            name = name[1:]
        return Module(name, [x[0] for x in m[1:]], symbol)


def propagate(src: Module, pulse: bool, modules: dict[str, Module]):
    outputs = []
    for m in [modules[m] for m in src.targets]:
        # print(f"{src.name} -> {'H' if pulse else 'L'} -> {m.name}")
        if m.symbol == "%":
            if not pulse:
                m.is_on = not m.is_on
                outputs.append((m, m.is_on))
        elif m.symbol == "&":
            m.inputs[src.name] = pulse
            m.is_on = not all(m.inputs.values())
            outputs.append((m, m.is_on))
        else:
            outputs.append((m, pulse))
    return outputs


def run_network(i: int, modules: dict[str, Module], button: Module):
    # print(f"---[Run {i+1}]---")
    pulses_lo, pulses_hi = 1, 0
    outputs = propagate(button, False, modules)
    while outputs:
        pulses_lo += sum(len(ou[0].targets) for ou in outputs if not ou[1])
        pulses_hi += sum(len(ou[0].targets) for ou in outputs if ou[1])
        outputs = [
            x for a in [propagate(op[0], op[1], modules) for op in outputs] for x in a
        ]
    # print("  ---[Flip-flops]---")
    # for ff in [m for m in modules.values() if m.symbol == "%"]:
    #    print(f"  {ff.name}: {'1' if ff.on else '0'}")
    # print("  ---[pulses]---")
    # print(f"  lo: {pulses_lo}")
    # print(f"  hi: {pulses_hi}")
    # print("------------------")
    # ffstate = ["1" if ff.on else "0" for ff in modules.values() if ff.symbol == "%"]
    # print(f"run {i+1}: ff = {''.join( ffstate )}, cnts = {pulses_lo}, {pulses_hi}")
    return pulses_lo, pulses_hi


def fast_run_network(modules: dict[str, Module], button: Module):
    outputs = propagate(button, False, modules)
    while outputs:
        outputs = [
            x for a in [propagate(op[0], op[1], modules) for op in outputs] for x in a
        ]


def parse_modules(data: list[str]):
    modules = {m.name: m for m in map(Module.parse, data)}
    modules["button"] = Module("button", ["broadcaster"], "")

    for conj in [m for m in modules.values() if m.symbol == "&"]:
        for src in [m for m in modules.values() if conj.name in m.targets]:
            conj.inputs[src.name] = False

    all_targets = [x for lst in [m.targets for m in modules.values()] for x in lst]
    for unlinked in [n for n in all_targets if n not in modules]:
        modules[unlinked] = Module(unlinked, [], "")

    return modules


def prob_1(data: list[str]):
    modules = parse_modules(data)
    pulses_lo, pulses_hi = 0, 0
    button = modules["button"]

    for i in range(1000):
        plo, phi = run_network(i, modules, button)
        pulses_lo += plo
        pulses_hi += phi

    return pulses_lo * pulses_hi


def prob_2(data: list[str]):
    modules = parse_modules(data)
    button = modules["button"]

    # Find the master target (module with no outputs)
    master_target = next(m for m in modules.values() if not m.targets)

    # This will be rm, which feeds into rx. It's a conjunction, meaning
    # all its inputs must be high to send out a low.
    t1 = next(m for m in modules.values() if master_target.name in m.targets)

    # These are the 4 conjunctions that feed into rm. We need all their outputs to be high
    # which means each must have at least 1 low input
    t2 = [m for m in modules.values() if t1.name in m.targets]

    # These are the 4 conjunctions that feed into the t2 conjunctions. We need all these to be low
    # so all their inputs must be high
    t3 = [m for m in modules.values() for t in t2 if t.name in m.targets]

    i = 0
    while True:
        i += 1
        fast_run_network(modules, button)
        if not i % 100000:
            print(f"i = {i}")
        for t in [t for t in t2 if t.is_on]:
            print(f'i = {i}: {"".join(str(t.is_on) for t in t2)}')


def main():
    with open(INPUT or "input.txt", mode="r", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    start = time.perf_counter()
    result = prob_1(data) if PART == 1 else prob_2(data)
    elapsed = time.perf_counter() - start

    print(f"Problem {PART}: {result}")
    print(f"Time: {elapsed} s")


if __name__ == "__main__":
    main()
