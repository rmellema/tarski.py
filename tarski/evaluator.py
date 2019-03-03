"""
This module allows for the evaluation of the formulas in :py:mod:`.formula` using the models from
:py:mod:`.model` or the worlds from :py:mod:`.world`. It also contains the code for defining
:py:class:`.Assignment` functions.

Using this module it is also possible to define your own evaluators, by creating a subclass of
:py:class:`BaseEvaluator`.
"""
from abc import ABC, abstractmethod as abstract

class EvaluateError(Exception):
    """
    An exception that can get thrown during evaluation of a formula.
    """

class PredicateError(Exception):
    """
    An exception that gets thrown for undefined predicates.
    """
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return "No Predicate with name: " + self.name

class PartialAssingment(EvaluateError):
    """
    An exception that gets throw if a certain key cannot be found in the assignment.
    """
    def __init__(self, assignment, key):
        super().__init__()
        self.assignment = assignment
        self.key = key

    def __str__(self):
        return "No binding found for: " + self.key

class IncompleteEvaluator(EvaluateError):
    """
    An exception that gets throw if an evaluator does not implement the evaluation of a formula.
    """
    def __init__(self, evaluator, formula):
        super().__init__()
        self.evaluator = evaluator
        self.formula = formula

    def __str__(self):
        return '{} cannot evaluate {}'.format(self.evaluator.__class__.__name__, str(self.formula))

def class2function(name):
    "Transform a class name into snake case for use in ``getattr``."
    result = name[0].lower()
    for char in name[1:]:
        if char.isupper():
            result += '_' + char.lower()
        else:
            result += char
    return result

class Assignment:
    """
    This class represents an assignment function for variables. It can be based upon an other
    assignment to "copy" its values. All the other given values are applied to the assignment.

    :param Assignment _prev: The assignment to base this one of off.
    """
    def __init__(self, _prev=None, **kwargs):
        self.store = {}
        self.prev = _prev
        for key in kwargs:
            self[key] = kwargs[key]

    def __missing__(self, key):
        if self.prev:
            return self.prev[key]
        raise PartialAssingment(self, key)

    def __iter__(self):
        return AssignmentIterator(self)

    def __str__(self):
        return '{' + ', '.join('(' + str(k) + ', ' + str(self[k]) + ')' for k in self) + '}'

    def __getitem__(self, key):
        try:
            return self.store[key]
        except KeyError:
            if self.prev:
                return self.prev[key]
            raise PartialAssingment(self, key) from None

    def __setitem__(self, key, value):
        self.store[key] = value

    def scope(self, **kwargs):
        """
        Create a new :py:class:`.Assignment` based on this one. All the arguments given are
        directly applied to the new :py:class:`.Assignment`. This is the prefered way of making new
        Assignments.
        """
        return Assignment(_prev=self, **kwargs)

class AssignmentIterator:
    """
    An Iterator to iterate over the keys in an assignment.

    :param Assignment assignment: The assignment to iterate over.
    """
    def __init__(self, assignment):
        self.assignment = assignment
        self.used = set()
        self.second = False
        self._iter = iter(self.assignment.store)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            k = self._iter.__next__()
            if k in self.used:
                return self.__next__()
            self.used.add(k)
            return k
        except StopIteration:
            if self.second or not self.assignment.prev:
                raise
            self._iter = iter(self.assignment.prev)
            self.second = True
            return self.__next__()

class BaseEvaluator(ABC):
    """
    The class to base all other Evaluators of off. This class cannot be instantiated itself.
    """
    def evaluate(self, structure, formula, assignment=Assignment()):
        """
        Evaluate the given ``formula`` in the given ``structure`` under ``assignment``.

        :param structure: The structure to evaluate the ``formula`` in. Needs to have an attribute
        called ``domain`` if the formula has quanitfiers.
        :param Formula formula: The formula to evaluate.
        :param Assignment assignment: The assignment to use. Defaults to the empty assignment.
        :returns: True if the formula is valid in the given structure under the assignment, False
        otherwise.
        """
        try:
            func = getattr(self, "evaluate_" + class2function(formula.__class__.__name__))
            return func(structure, formula, assignment)
        except AttributeError:
            raise IncompleteEvaluator(self, formula) from None

    @abstract
    def interpret(self, name, structure, assignment):
        """
        Translate the given ``name`` to an object in ``structure`` by looking it up in either the
        ``structure`` or the ``assignment``.

        :param str name: The name of the object to look up.
        :param structure: The structure in which the object should exist.
        :param Assignment assignment: The assignment to be used if ``name`` is a variable.
        """

    @abstract
    def evaluate_predicate(self, structure, predicate, assignment):
        """
        Evaluate the given ``predicate`` in the given ``structure`` under ``assignment``.

        :param structure: The structure to evaluate the ``formula`` in.
        :param Predicate predicate: The predicate to evaluate.
        :param Assignment assignment: The assignment to use.
        :returns: True if the formula is valid in the given structure under the assignment, False
        otherwise.
        """

    def evaluate_not(self, structure, formula, assignment):
        """
        Evaluate the given ``formula`` in the given ``structure`` under ``assignment``.

        :param structure: The structure to evaluate the ``formula`` in.
        :param Not formula: The formula to evaluate.
        :param Assignment assignment: The assignment to use.
        :returns: True if the formula is valid in the given structure under the assignment, False
        otherwise.
        """
        return not self.evaluate(structure, formula.formula, assignment)

    def evaluate_and(self, structure, formula, assignment):
        """
        Evaluate the given ``formula`` in the given ``structure`` under ``assignment``.

        :param structure: The structure to evaluate the ``formula`` in.
        :param And formula: The formula to evaluate.
        :param Assignment assignment: The assignment to use.
        :returns: True if the formula is valid in the given structure under the assignment, False
        otherwise.
        """
        return all(self.evaluate(structure, conjunct, assignment)
                   for conjunct in formula.conjuncts)

    def evaluate_or(self, structure, formula, assignment):
        """
        Evaluate the given ``formula`` in the given ``structure`` under ``assignment``.

        :param structure: The structure to evaluate the ``formula`` in.
        :param Or formula: The formula to evaluate.
        :param Assignment assignment: The assignment to use.
        :returns: True if the formula is valid in the given structure under the assignment, False
        otherwise.
        """
        return any(self.evaluate(structure, disjunct, assignment)
                   for disjunct in formula.disjuncts)

    def evaluate_implication(self, structure, formula, assignment):
        """
        Evaluate the given ``formula`` in the given ``structure`` under ``assignment``.

        :param structure: The structure to evaluate the ``formula`` in.
        :param Implication formula: The formula to evaluate.
        :param Assignment assignment: The assignment to use.
        :returns: True if the formula is valid in the given structure under the assignment, False
        otherwise.
        """
        return not self.evaluate(structure, formula.antecedent, assignment) or \
                self.evaluate(structure, formula.consequent, assignment)

    def evaluate_bi_implication(self, structure, formula, assignment):
        """
        Evaluate the given ``formula`` in the given ``structure`` under ``assignment``.

        :param structure: The structure to evaluate the ``formula`` in.
        :param BiImplication formula: The formula to evaluate.
        :param Assignment assignment: The assignment to use.
        :returns: True if the formula is valid in the given structure under the assignment, False
        otherwise.
        """
        return self.evaluate(structure, formula.left, assignment) == \
                self.evaluate(structure, formula.right, assignment)

    def evaluate_for_all(self, structure, formula, assignment):
        """
        Evaluate the given ``formula`` in the given ``structure`` under ``assignment``.

        :param structure: The structure to evaluate the ``formula`` in.
        :param ForAll formula: The formula to evaluate.
        :param Assignment assignment: The assignment to use.
        :returns: True if the formula is valid in the given structure under the assignment, False
        otherwise.
        """
        var = formula.variable
        form = formula.formula
        return all(self.evaluate(structure, form, assignment.scope(**{var: obj}))
                   for obj in structure.domain)

    def evaluate_exists(self, structure, formula, assignment):
        """
        Evaluate the given ``formula`` in the given ``structure`` under ``assignment``.

        :param structure: The structure to evaluate the ``formula`` in.
        :param Exists formula: The formula to evaluate.
        :param Assignment assignment: The assignment to use.
        :returns: True if the formula is valid in the given structure under the assignment, False
        otherwise.
        """
        var = formula.variable
        form = formula.formula
        return any(self.evaluate(structure, form, assignment.scope(**{var: obj}))
                   for obj in structure.domain)

class ModelEvaluator(BaseEvaluator):
    "An evaluator that evaluates predicates using a :py:class:`~.model.Model`."
    def interpret(self, name, structure, assignment):
        try:
            return structure.constants[name]
        except KeyError:
            return assignment[name]

    def evaluate_predicate(self, structure, predicate, assignment):
        args = tuple(self.interpret(var, structure, assignment) for var in predicate.args)
        try:
            return args in structure.predicates[predicate.name]
        except KeyError:
            raise PredicateError(predicate.name) from None
