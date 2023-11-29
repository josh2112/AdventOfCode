SAMPLE = 0

with open("input-sample.txt" if SAMPLE else "input.txt", "r") as f:
    m = {}
    for line in f.readlines():
        k, op = [t.strip() for t in line.split(":")]
        if op.find(" ") > 0:
            m[k] = [t.strip() for t in op.split()]
        else:
            m[k] = int(op)

unsolved = [k for k in m if not isinstance(m[k], int)]

while unsolved:
    for k in unsolved:
        a, op, b = m[k]
        if a not in unsolved and b not in unsolved:
            a, b = m[a], m[b]
            if op == "+":
                m[k] = a + b
            elif op == "-":
                m[k] = a - b
            elif op == "*":
                m[k] = a * b
            elif op == "/":
                m[k] = a / b
            unsolved.remove(k)

print(m["root"])
