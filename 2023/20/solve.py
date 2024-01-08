#!/usr/bin/env python3

import dataclasses
import re
import time
import math

# https://adventofcode.com/2023/day/20

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 2


@dataclasses.dataclass
class Module:
    name: str
    targets: list["Module"]
    symbol: str
    is_on: bool = False
    inputs: dict["Module", bool] = dataclasses.field(default_factory=dict)
    
    def __hash__(self) -> int:
        return hash( self.name )

    def propagate(self, pulse: bool):
        outputs = []
        for m in self.targets:
            #print(f"{self.name} -> {'H' if pulse else 'L'} -> {m.name}")
            if m.symbol == "%":
                if not pulse:
                    m.is_on = not m.is_on
                    outputs.append((m, m.is_on))
            elif m.symbol == "&":
                m.inputs[self] = pulse
                m.is_on = not all(m.inputs.values())
                outputs.append((m, m.is_on))
            else:
                outputs.append((m, pulse))
        return outputs


def parse_modules(data: list[str]):
    defs = [[m[0] for m in re.finditer(r"([^\s\->,])+", line)] for line in data]
    modules = {m.name: m for m in [Module( d[0][1:] if not d[0][0].isalpha() else d[0], [], d[0][0] if not d[0][0].isalpha() else '' ) for d in defs]}
    
    for m in list(modules.values()):
        for t in next( d[1:] for d in defs if d[0] == m.symbol + m.name ):
            if t not in modules:
                modules[t] = Module( t, [], '' )
            m.targets.append(modules[t] )

    modules["button"] = Module("button", [modules["broadcaster"]], "")

    for conj in [m for m in modules.values() if m.symbol == "&"]:
        for src in [m for m in modules.values() if conj in m.targets]:
            conj.inputs[src] = False

    return modules


def prob_1(data: list[str]):
    modules = parse_modules(data)
    pulses_lo, pulses_hi = 0, 0
    button = modules["button"]

    for i in range(1000):
        #print(f"---[Run {i+1}]---")
        outputs = button.propagate(False)
        pulses_lo += 1
        while outputs:
            pulses_lo += sum(len(ou[0].targets) for ou in outputs if not ou[1])
            pulses_hi += sum(len(ou[0].targets) for ou in outputs if ou[1])
            outputs = [
                x for a in [op[0].propagate(op[1]) for op in outputs] for x in a
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

    return pulses_lo * pulses_hi


def prob_2(data: list[str]):
    modules = parse_modules(data)

    # From visual inspection, there are actually 4 subgraphs. Each gets 1 input from broadcaster
    # which runs through a network of flip-flops, finally ending at a conjunction feeding into
    # another conjunction. These outer 4 conjunctions, from each network, feed into another conj
    # which feeds into the master target.
    #
    # So, for each of the subgraphs, figure out when all of the flip-flops must be high. Then figure
    # out when all networks will have this condition simultaneously.

    # entry flipflop and exit conjunction
    Network = tuple[Module,Module]
    networks: list[Network] = []

    # Find the flip-flops making up each network. Starting with each broadcaster output, walk the
    # tree until we see a conjunction. Isolate the subnetworks too: When we find the conjuction,
    # disconnect its non-flip-fop targets.
    for start in modules["broadcaster"].targets:
        stack: set[Module] = set( [start] )
        ffs = set()
        end = None
        while stack:
            ff = stack.pop()
            if ff not in ffs:
                ffs.add( ff )
                stack.update( t for t in ff.targets if t.symbol == '%' )
                # If we find the conjuction, disconnect it
                if conj := next( (t for t in ff.targets if t.symbol == '&'), None ):
                    end = conj
                    end.targets = [m for m in end.targets if m.symbol != '&']
        networks.append( (start, end )) # type: ignore (end will be non-null)

    counts: dict[Module,int] = {}

    
    for entry_ff, exit_conj in networks:
        count = 0
        start = Module( "start", [entry_ff], '' )
        
        got_it = False
        while True and not got_it:
            count += 1
            outputs = [(start,False)]
            while outputs and not got_it:
                outputs = [
                    x for a in [op[0].propagate(op[1]) for op in outputs] for x in a
                ]
                # Did our conjunction get a low pulse yet??
                if (exit_conj,False) in outputs:
                    got_it = True
        
        counts[exit_conj] = count
    
    return math.lcm( *counts.values())

def make_graphviz_file(data):
    modules = parse_modules(data)
    with open("graph.dot", "w") as f:
        f.write( "digraph Day20 {\n" )
        for m in modules.values():
            f.write(f'{m.name} [label="{m.symbol}{m.name}", shape="{'rect' if m.symbol == '&' else 'ellipse'}"]\n')
        for m in modules.values():
            if m.targets:
                f.write(
                    f"{m.name} -> {', '.join( t.name for t in m.targets )}\n"
                )
        f.write( "broadcaster [shape=Mdiamond];\n")
        f.write( "rx [shape=Mdiamond];\n")
        f.write( "}" )


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
