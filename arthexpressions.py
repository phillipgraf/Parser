"""
>>> print(result(ParseAExpr().parse("42")))
42
>>> print(result(ParseAExpr().parse("x")))
x
>>> print(result(ParseAExpr().parse("x + 2*y")))
(x + (2 * y))
>>> print(result(ParseAExpr().parse("15 + x * x")))
(15 + (x * x))
>>> print(result(ParseAExpr().parse("x + y + z")))
(x + (y + z))
"""

from pcomb import *
from z3 import *

"""
<arithm_expression> ::= <term> ’+’ <arithm_expression> | <term>
<term>              ::= <factor> ’*’ <term> | <factor>
<factor>            ::= ’(’ <arithm_expression> ’)’ | <int> | <variable>
<int>               ::= INTEGER
<variable>          ::= IDENTIFIER
"""


class ParseAExpr(Parser):
    def __init__(self):
        self.parser = ParsePlus() ^ ParseTerm()


class ParseTerm(Parser):
    def __init__(self):
        self.parser = ParseTimes() ^ ParseFactor()


class ParseFactor(Parser):
    def __init__(self):
        self.parser = ParseParen() ^ ParseInteger() ^ ParseVar()


class ParseVar(Parser):
    def __init__(self):
        self.parser = ParseIdent() >> (lambda name:
                                       Return(AVar(name)))


class ParseInteger(Parser):
    def __init__(self):
        self.parser = ParseInt() >> (lambda n:
                                     Return(Int(n)))


class ParseParen(Parser):
    def __init__(self):
        self.parser = ParseSymbol('(') >> (lambda _:
                                           ParseAExpr() >> (lambda e:
                                                            ParseSymbol(')') >> (lambda _:
                                                                                 Return(e))))


class ParsePlus(Parser):
    def __init__(self):
        self.parser = ParseTerm() >> (lambda t:
                                      ParseSymbol('+') >> (lambda _:
                                                           ParseAExpr() >> (lambda e:
                                                                            Return(Plus(t, e)))))


class ParseTimes(Parser):
    def __init__(self):
        self.parser = ParseFactor() >> (lambda x:
                                        ParseSymbol('*') >> (lambda _:
                                                             ParseTerm() >> (lambda y:
                                                                             Return(Times(x, y)))))


class Expr:
    def __add__(self, other):
        return Plus(self, other)

    def __mul__(self, other):
        return Times(self, other)


class Int(Expr):
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return str(self.val)

    def ev(self, env):
        return self.val

    def toZ3(self):
        return self.val


class AVar(Expr):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def ev(self, env):
        return env[self.name]

    def toZ3(self):
        return z3.Int(self.name)


class BinOp(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} {self.op} {self.right})"

    def ev(self, env):
        return self.fun(self.left.ev(env), self.right.ev(env))

    def toZ3(self):
        return f"{self.left} {self.op} {self.right}"


class Plus(BinOp):
    name = "Plus"
    fun = lambda _, x, y: x + y
    op = '+'

    def toZ3(self):
        return (self.left.toZ3() + self.right.toZ3())


class Times(BinOp):
    name = "Times"
    fun = lambda _, x, y: x * y
    op = '*'

    def toZ3(self):
        return (self.left.toZ3() * self.right.toZ3())
