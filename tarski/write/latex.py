"""
The output writer for LaTeX output of the first-order structure.
"""
from . import AbstractModelWriter
from .util import make_pair

class LaTeXModelWriter(AbstractModelWriter):
    """
    The LaTeX output writer. The resulting LaTeX output will require the amsmath package.
    """
    format_name = 'latex'
    format_description = 'Write the Model to a TeXable representation.'

    def make_identifier(self, value):
        """
        Turn an identifier in the model into a string.
        """
        return "\\delta_{{{}}}".format(value)

    def write_domain(self, domain):
        """
        Write the domain to the stream.
        """
        self.stream.write("\\begin{align*}\n\tD &= \\left\\{")
        self.stream.write(', '.join(self.make_identifier(id) for id in domain))
        self.stream.write('\\right\\}\n\\end{align*}')

    def write_constant(self, constant, identifier):
        """
        Write a single constant to the stream.
        """
        self.stream.write('(')
        self.stream.write(constant)
        self.stream.write(')^{\\mathfrak{M}} &= ')
        self.stream.write(self.make_identifier(identifier))
        self.stream.write(r'\\')

    def write_constants(self, constants):
        """
        Write all the constants to the stream.
        """
        self.stream.write('\\begin{align*}\n')
        super().write_constants(constants)
        self.stream.write('\\end{align*}\n')

    def write_predicate(self, name, extension):
        """
        Write a predicat to the stream.
        """
        self.stream.write(r"\mathfrak{M}(\mathit{")
        self.stream.write(name)
        self.stream.write(r"}) &= \left\{ ")
        self.stream.write(', '.join(make_pair((self.make_identifier(id) for id in pair),
                                              '\\langle', '\\rangle')
                                    for pair in extension))
        self.stream.write(r"\right\}\\")

    def write_predicates(self, predicates):
        """
        Write the predicates to the stream.
        """
        self.stream.write('\\begin{align*}\n')
        super().write_predicates(predicates)
        self.stream.write('\\end{align*}\n')
