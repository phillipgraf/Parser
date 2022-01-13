"""
>>> printExpr("x = y")
(x = y)
>>> printExpr("x + 2 * y")
(x + (2 * y))
>>> printExpr("x < 2 and y < 1")
((x < 2) and (y < 1))
>>> printExpr("(x + 2*y < 15 + x * x) or z = 5")
(((x + (2 * y)) < (15 + (x * x))) or (z = 5))
>>> printExpr("x + 2*y < 15 + x * x or z = 5")
(((x + (2 * y)) < (15 + (x * x))) or (z = 5))
>>>
>>> env = {'x':1, 'y':2, 'z':3}
>>> evalExpr("x = y", env)
False
>>> evalExpr("x + 2 * y", env)
5
>>> evalExpr("x < 2 and y < 1", env)
False
>>> evalExpr("(x + 2*y < 15 + x * x) or z = 5", env)
True
>>> evalExpr("x + 2*y < 15 + x * x or z = 5", env)
True
>>> evalExpr("x * 2 + 3 < x * (2 + 3)", env)
False
>>> evalExpr("y * 2 + 3 < y * (2 + 3)", env)
True
"""

from boolexpressions import *

"""
<expr> ::= <boolean_expression> | <arithm_expression>
"""


class ParseExpr(Parser):
    def __init__(self):
        self.parser = ParseBExpr() ^ ParseAExpr()


def printExpr(inp):
    print(result(ParseExpr().parse(inp)))


def evalExpr(inp, env):
    print(result(ParseExpr().parse(inp)).ev(env))
