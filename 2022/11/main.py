import math


class Monkey:
    def __init__(self, items, op, test, throwto):
        self.items, self.op, self.test, self.throwto = items, op, test, throwto
        self.total_inspections = 0

    def process(self, monkeys, worrylevel_divisor):
        # print(f"Monkey {monkeys.index( self )}")
        for item in self.items:
            self.total_inspections += 1
            worrylevel = math.floor(eval(self.op, {"old": item}) // worrylevel_divisor)
            worrylevel %= mod
            target = 1 if worrylevel % self.test else 0
            monkeys[self.throwto[target]].items.append(worrylevel)
            # print(f"  worry level {worrylevel}, goes to monkey {self.throwto[target]}")
        self.items = []


with open("input.txt", "r") as f:
    lines = f.readlines()
    monkeys = []
    for m in [lines[i + 1 : i + 6] for i in range(0, len(lines) + 1, 7)]:
        items = [int(i.strip()) for i in m[0].split(":")[1].strip().split(",")]
        op = m[1].split("=")[1].strip()
        test = int(m[2].split()[-1])
        throwto = [int(m[i].split()[-1]) for i in (3, 4)]
        monkeys.append(Monkey(items, op, test, throwto))
    mod = math.prod(m.test for m in monkeys)
    for m in monkeys:
        m.mod = mod


def calc_monkeybusiness(num_rounds, worrylevel_divisor):
    for i in range(num_rounds):
        print("round", i)
        for m in monkeys:
            m.process(monkeys, worrylevel_divisor)

    insp = sorted(m.total_inspections for m in monkeys)[-2:]
    print(insp[0] * insp[1])


part1 = lambda: calc_monkeybusiness(20, 3)
part2 = lambda: calc_monkeybusiness(10000, 1)

# part1()
part2()
