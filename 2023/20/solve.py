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
    on: bool = False
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
        if m.name == "rx" and not pulse:
            pass
        if m.symbol == "%":
            if not pulse:
                m.on = not m.on
                output = 1 if m.on else 0
                outputs.append((m, output))
        elif m.symbol == "&":
            m.inputs[src.name] = pulse
            outputs.append((m, not all(m.inputs.values())))
        else:
            outputs.append((m, pulse))
    return outputs


def run_network(i: int, modules: dict[str, Module]):
    # print(f"---[Run {i+1}]---")
    pulses_lo, pulses_hi = 1, 0
    outputs = propagate(modules["button"], False, modules)
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
    ffstate = ["1" if ff.on else "0" for ff in modules.values() if ff.symbol == "%"]
    # print(f"run {i+1}: ff = {''.join( ffstate )}, cnts = {pulses_lo}, {pulses_hi}")
    return ffstate, pulses_lo, pulses_hi


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
    for i in range(1000):
        _, plo, phi = run_network(i, modules)
        pulses_lo += plo
        pulses_hi += phi

    return pulses_lo * pulses_hi

@dataclasses.dataclass
class State:
    module: Module
    pulse_in: bool


def prob_2(data: list[str]):
    modules = parse_modules(data)

    # Find the master target (module with no outputs)
    master_target = next(m for m in modules.values() if not m.targets)

    # Work backward until we find all the flip-flops (and their states) which will
    # send this module a low pulse
    states = [State(master_target, False)]
    
    while any( s for s in states if s.module.symbol != "%"):
        # For each module that's not a flip-flop...
        for state in [state for state in states if state.module.symbol != "%"]:
            # Find the modules that output to it
            inputs = [m for m in modules.values() if state.module.name in m.targets]
            # For each of those, figure out what its input has to be to cause the desired
            # output (state.input)
            for m in inputs:
                if m.symbol == "&":
                    # Inputs must be all high
                    pass
            states.remove( state )


    num_presses = 0
    for i in range(1000):
        ffstates, _, _ = run_network(num_presses, modules)
        print("".join(ffstates))


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
