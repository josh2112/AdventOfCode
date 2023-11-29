SAMPLE = 0

with open("input-sample.txt" if SAMPLE else "input.txt", "r") as f:
    m = {}
    for line in f.readlines():
        k, op = [t.strip() for t in line.split(":")]
        if op.find(" ") > 0:
            m[k] = [t.strip() for t in op.split()]
        else:
            m[k] = int(op)

m["root"][1] = "="
m["humn"] = "humn"

unsolved = [k for k in m if isinstance(m[k], list)]
# unsolved.remove("humn")

reduced = True
while unsolved and reduced:
    reduced = False
    for k in unsolved:
        a, op, b = m[k]
        if a not in unsolved and b not in unsolved:
            a, b = m[a], m[b]
            if isinstance(a, str) or isinstance(b, str):
                continue
            if op == "+":
                m[k] = a + b
            elif op == "-":
                m[k] = a - b
            elif op == "*":
                m[k] = a * b
            elif op == "/":
                m[k] = a / b
            unsolved.remove(k)
            reduced = True

for k in unsolved:
    a, op, b = m[k]
    if a not in unsolved:
        m[k][0] = m[a]
    if b not in unsolved:
        m[k][2] = m[b]

# for k in m:
#    print(f"{k}: {m[k]}")


def substitute(q):
    if q != "humn":
        if isinstance(q[0], str):
            q[0] = substitute(m[q[0]])
        if isinstance(q[2], str):
            q[2] = substitute(m[q[2]])
    return q


isnum = lambda x: isinstance(x, (int, float))

eq = substitute(m["root"])

a = eq[0] if isnum(eq[0]) else eq[2]
b = eq[0] if eq[0] != a else eq[2]

print(f"{a} = {b}")

while isinstance(b, list):
    x = b[0] if isnum(b[0]) else b[2]
    eq = b[0] if b[0] != x else b[2]
    if b[1] == "+":
        a -= x
    elif b[1] == "-":
        if x == b[2]:
            a += x
        else:
            a = -a + x
    elif b[1] == "*":
        a /= x
    elif b[1] == "/":
        if x == b[2]:
            a *= x
        else:
            a = x / a
    b = eq

print(f"{a} = {b}")
