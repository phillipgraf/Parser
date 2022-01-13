"""
>>> print(result(ParseBExpr().parse("x = z")))
(x = z)
>>> print(result(ParseBExpr().parse("x = z")).toZ3())
x == z
>>> print(result(ParseBExpr().parse("x < 15 and 7 < x")))
((x < 15) and (7 < x))
>>> print(result(ParseBExpr().parse("x < 15 or 20 < x")))
((x < 15) or (20 < x))
"""

from arthexpressions import *

"""
<boolean_expression> ::= <disjunct> ’or’ <boolean_expression> | <disjunct>
<disjunct> ::= <conjunct> ’and’ <disjunct> | <conjunct>
<conjunct> ::= <arithmetic_expression> <cmp> <arithmetic_expression> | (<boolean_expression>)
<cmp> ::= ’=’ | ’<’
"""


class ParseBExpr(Parser):
    def __init__(self):
        self.parser = ParseOr() ^ ParseDisj()


class ParseDisj(Parser):
    def __init__(self):
        self.parser = ParseAnd() ^ ParseConj()


class ParseConj(Parser):
    def __init__(self):
        self.parser = ParseComp() ^ ParseBParen()


class ParseComp(Parser):
    def __init__(self):
        self.parser = ParseEquals() ^ ParseSmaller()


class ParseEquals(Parser):
    def __init__(self):
        self.parser = ParseAExpr() >> (lambda d:
                                       ParseSymbol("=") >> (lambda _:
                                                            ParseAExpr() >> (lambda e:
                                                                             Return(Equals(d, e)))))


class ParseSmaller(Parser):
    def __init__(self):
        self.parser = ParseAExpr() >> (lambda d:
                                       ParseSymbol("<") >> (lambda _:
                                                            ParseAExpr() >> (lambda e:
                                                                             Return(Smaller(d, e)))))


class ParseBVar(Parser):
    def __init__(self):
        self.parser = ParseIdentifier() >> (lambda name:
                                            Return(BVar(name)))


class ParseBParen(Parser):
    def __init__(self):
        self.parser = ParseSymbol("(") >> (lambda _:
                                           ParseBExpr() >> (lambda e:
                                                            ParseSymbol(")") >> (lambda _:
                                                                                 Return(e))))


class ParseOr(Parser):
    def __init__(self):
        self.parser = ParseDisj() >> (lambda d:
                                      ParseSymbol("or") >> (lambda _:
                                                            ParseBExpr() >> (lambda e:
                                                                             Return(Or(d, e)))))


class ParseAnd(Parser):
    def __init__(self):
        self.parser = ParseConj() >> (lambda x:
                                      ParseSymbol("and") >> (lambda _:
                                                             ParseDisj() >> (lambda y:
                                                                             Return(And(x, y)))))


class BExpr:
    pass


class BVar(BExpr):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def ev(self, env):
        return env[self.name]

    def toZ3(self):
        return z3.Bool(self.name)


class Op2(BExpr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} {self.op} {self.right})"

    def ev(self, env):
        return self.fun(self.left.ev(env), self.right.ev(env))

    def toZ3(self):
        return f"{self.left} {self.op} {self.right}"


class Or(Op2):
    op = "or"
    fun = lambda _, x, y: x or y

    def toZ3(self):
        return z3.Or(self.left.toZ3(), self.right.toZ3())


class And(Op2):
    op = "and"
    fun = lambda _, x, y: x and y

    def toZ3(self):
        return z3.And(self.left.toZ3(), self.right.toZ3())


class Equals(Op2):
    op = "="
    fun = lambda _, x, y: x == y

    def toZ3(self):
        return (self.left.toZ3() == self.right.toZ3())
        # return eval(f"{self.left.toZ3()} == {self.right.toZ3()}")


class Smaller(Op2):
    op = "<"
    fun = lambda _, x, y: x < y

    def toZ3(self):
        return (self.left.toZ3() < self.right.toZ3())
