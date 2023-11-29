SAMPLE = 1

with open("input-sample.txt" if SAMPLE else "input.txt", "r") as f:
    n = [int(x.strip()) for x in f.readlines()]

nlen = len(n)
c, i = 0, 0

print(n)

while c < nlen - 1:
    if n[i] != 0:
        j = (i + n[i] + 1) % nlen
        print(f"inserting {n[i]} (idx {i}) at index {j} ({n[j]})")
        n.insert(j, n[i])
        del n[i]
        if j > i:
            i -= 1
    print(n)
    i += 1
    c += 1
