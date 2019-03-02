"""
The output writer for LaTeX output of the first-order structure.
"""
from . import AbstractModelWriter
from .util import make_pair

class LaTeXModelWriter(AbstractModelWriter):
    """
    The LaTeX output writer. The resulting LaTeX output is not a full document, so it can be
    included in documents. It depends on `amsmath`, `amssymb`, and `breqn`, and you need to include
    the following lines in the preamble of your latex document::

        \\DeclareFlexCompoundSymbol{\\mycomb}{Bin}{}
        \\newcommand{\\mycom}{,\\mycomb}
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
        self.stream.write("\\begin{dmath*}\n\tD = \\left\\{")
        self.stream.write('\\mycom '.join(self.make_identifier(id) for id in domain))
        self.stream.write('\\right\\}\n\\end{dmath*}')

    def write_constant(self, constant, identifier):
        """
        Write a single constant to the stream.
        """
        self.stream.write('\\begin{dmath*}')
        self.stream.write('{')
        self.stream.write(constant)
        self.stream.write('}^{\\mathfrak{M}} = ')
        self.stream.write(self.make_identifier(identifier))
        self.stream.write(r'\end{dmath*}')

    def write_predicate(self, name, extension):
        """
        Write a predicate to the stream.
        """
        self.stream.write(r"\begin{dmath*}")
        self.stream.write(r"\mathfrak{M}(\mathit{")
        self.stream.write(name)
        self.stream.write(r"}) = ")
        if extension:
            self.stream.write(r"\left\{ ")
            self.stream.write(r'\mycom '.join(make_pair((self.make_identifier(id) for id in pair),
                                                        '\\langle', '\\rangle')
                                              for pair in extension))
            self.stream.write(r"\right\}")
        else:
            self.stream.write(r"\emptyset")
        self.stream.write(r"\end{dmath*}")

    def write_model(self, model):
        """
        Write the model to the stream. Makes sure that all the `=` signs in the equations are
        aligned by wrapping all equations in a `dgroup*`.

        :param Model model: The model to write to the stream.
        """
        self.stream.write('\\begin{dgroup*}\n')
        super().write_model(model)
        self.stream.write('\\end{dgroup*}\n')
