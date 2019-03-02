"""
A module for representing first order logical formulas, as given in Language, Proof, and Logic by
Barwise and Etchmody.

Formulas can be created using the classes described in this module. For convenience, conjunctions,
disjunctions, and negations can also be created using ``&``, ``|``, and ``~`` respectively. This
allows for the following more readable format::

    Predicate("Larger", 'a', 'x') & ~(Predicate("Smaller", 'c', 'x') | Predicate("Small", 'c'))

Besides the definitions for formulas, this module also contains functions for identifying constants
and variables, which are needed for the implementation of the method :py:meth:`~.Formula.vars`.
A variable is any string starting with one of the letters in :const:`VARIABLES`. This means that
``x`` is a valid variable, but so is ``x1``, or even ``_variable``.

.. py:attribute:: CONSTANTS

    The letters with which a valid constant may start.

.. py:attribute:: VARIABLES

    The letters with which a valid variable may start.
"""
from abc import ABC, abstractmethod as abstract
from functools import reduce

CONSTANTS = ('a', 'b', 'c', 'd', 'e', 'f')
VARIABLES = ('x', 'y', 'z', 'u', 'v', 'w', '_')

def is_constant(name):
    "A function used to determine if something is a constant."
    return name.startswith(CONSTANTS)

def is_variable(name):
    "A function to determine is something is a variable."
    return name.startswith(VARIABLES)

class Formula(ABC):
    """
    This class represents what a formula can do and should be used as a base class for all other
    formulas. You cannot directly create instances of this class.
    """
    def __inner_str__(self):
        "Return a string version of this formula with parenthesis if necessary."
        return '(' + str(self) + ')'

    @abstract
    def vars(self):
        "Get all the variables in this formula."

    def free_vars(self):
        "Get all of the free variables in this formula."
        return self.vars()

    @abstract
    def simplified(self):
        "Return a simplified but logically equivalent form of this formula."

    def __and__(self, other):
        return And(self, other).flattened()

    def __or__(self, other):
        return Or(self, other).flattened()

    def __invert__(self):
        return Not(self)

class Predicate(Formula):
    "A class to represent various predicates."
    def __init__(self, name, *args):
        self.name = name
        self.args = args

    def __inner_str__(self):
        return self.name + '(' + ','.join(self.args) + ')'

    def __str__(self):
        return self.__inner_str__()

    def simplified(self):
        return self # Nothing to simplify

    def vars(self):
        return frozenset(filter(is_variable, self.args))

class Not(Formula):
    "A class to represent the negation of a formula."
    def __init__(self, formula):
        self.formula = formula

    def __inner_str__(self):
        return '~' + self.formula.__inner_str__()

    def __str__(self):
        return self.__inner_str__()

    def simplified(self):
        if isinstance(self.formula, Not):
            return self.formula.formula.simplified()
        return Not(self.formula.simplified())

    def vars(self):
        return self.formula.vars()

class And(Formula):
    "A class to represent conjunctions of multiple formulas."
    def __init__(self, *args):
        self.conjuncts = args

    def __str__(self):
        return ' & '.join(c.__inner_str__() for c in self.conjuncts)

    def flattened(self):
        "Return a version of this formula where none of the conjuncts are a conjunction."
        conjuncts = []
        for conjunct in self.conjuncts:
            if isinstance(conjunct, And):
                conjuncts.extend(conjunct.flattened().conjuncts)
            else:
                conjuncts.append(conjunct)
        return And(*conjuncts)

    def simplified(self):
        conjuncts = set(conjunct.simplified() for conjunct in self.flattened().conjuncts)
        if len(conjuncts) == 1:
            return conjuncts.pop()
        return And(*conjuncts)

    def vars(self):
        return reduce(lambda a, b: a.union(b), (c.vars() for c in self.conjuncts))

class Or(Formula):
    "A class to represent disjunctions of multiple formulas."
    def __init__(self, *args):
        self.disjuncts = args

    def __str__(self):
        return ' | '.join(c.__inner_str__() for c in self.disjuncts)

    def flattened(self):
        "Return a version of this formula where none of the disjuncts are a disjunction."
        disjuncts = []
        for disjunct in self.disjuncts:
            if isinstance(disjunct, Or):
                disjuncts.extend(disjunct.flattened().disjuncts)
            else:
                disjuncts.append(disjunct)
        return Or(*disjuncts)

    def simplified(self):
        disjuncts = set(disjunct.simplified() for disjunct in self.flattened().disjuncts)
        if len(disjuncts) == 1:
            return disjuncts.pop()
        return Or(*disjuncts)

    def vars(self):
        return reduce(lambda a, b: a.union(b), (c.vars() for c in self.disjuncts))

class Implication(Formula):
    "A class to represent implications for formulas."
    def __init__(self, antecedent, consequent):
        self.antecedent = antecedent
        self.consequent = consequent

    def __str__(self):
        return self.antecedent.__inner_str__() + ' -> ' + self.consequent.__inner_str__()

    def simplified(self):
        return Implication(self.antecedent.simplified(), self.consequent.simplified())

    def vars(self):
        return self.antecedent.vars().union(self.consequent.vars())

class BiImplication(Formula):
    "A class to represent bi-implications for formulas."
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return self.left.__inner_str__() + ' <-> ' + self.right.__inner_str__()

    def simplified(self):
        return Implication(self.left.simplified(), self.right.simplified())

    def vars(self):
        return self.left.vars().union(self.right.vars())

class ForAll(Formula):
    "A class to represent the universal quantifier."
    def __init__(self, variable, formula):
        self.variable = variable
        self.formula = formula

    def __str__(self):
        return '@' + self.variable + ' '+ self.formula.__inner_str__()

    def simplified(self):
        return ForAll(self.variable, self.formula.simplied())

    def vars(self):
        return self.formula.vars().union((self.variable))

    def free_vars(self):
        return self.formula.free_vars().difference((self.variable))

class Exists(Formula):
    "A class to represent the existential quantifier."
    def __init__(self, variable, formula):
        self.variable = variable
        self.formula = formula

    def __str__(self):
        return '#' + self.variable + ' ' + self.formula.__inner_str__()

    def simplified(self):
        return ForAll(self.variable, self.formula.simplied())

    def vars(self):
        return self.formula.vars().union((self.variable))

    def free_vars(self):
        return self.formula.free_vars().difference((self.variable))
