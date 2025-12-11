from scipy.optimize import linprog

# Ex 1: (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
buttons = ((3,), (1, 3), (2,), (2, 3), (0, 2), (0, 1))
joltages = [3, 5, 4, 7]

# For each constraint j: 1 if button i includes j else 0
constraints = [[1 if j in b else 0 for b in buttons] for j in range(len(joltages))]

# solve
results = linprog(
    [1] * len(buttons),
    A_eq=constraints,
    b_eq=joltages,
    bounds=[(0, None) for i in constraints[0]],
    method="highs",
)

# print results
if results.status == 0:
    print(f"{int(results.fun)} ({results.x})")
