"""
>>> exprs = ["x + y +z = 10", "x < y", "x < 3", "0 < x"]
>>> sol = solve(exprs)
>>> sol
{’z = 5’, ’y = 3’, ’x = 2’}
>>> exprs = ["x + y +z = 10", "x < y", "x < 3", "5 < x"]
>>> sol = solve(exprs)
No solution!
"""
from generalexpressions import *


def solve(exprs):
    s = Solver()

    for i in exprs:
        s.add(result(ParseExpr().parse(i)).toZ3())

    if s.check() == sat:
        model = s.model()
        sol = set()
        for i in model:
            sol.add(f"{i} = {model[i]}")
        return sol
    else:
        print("No solution!")
        return None
