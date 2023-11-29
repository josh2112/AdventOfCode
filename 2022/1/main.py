totals = []

with open("input.txt", "r") as f:
    curcals = 0
    for cals in [int(l.strip()) if l.strip() else None for l in f.readlines()]:
        if cals:
            curcals += cals
        else:
            totals.append(curcals)
            curcals = 0

totals.sort()
print(sum(totals[-3:]))
