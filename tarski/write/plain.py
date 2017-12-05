"""
A Writer for writing to plain text output. It extends :py:class:`AbstractModelWriter`.
"""

from . import AbstractModelWriter
from .util import make_pair

class PlainModelWriter(AbstractModelWriter):
    """
    This writer takes models and writes them as plain text to the output.
    """
    format_name = 'plain'
    format_description = "Output the model to plain text"

    def make_identifier(self, value):
        """
        Turn a block into an easily printable identifier.
        """
        return 'd' + str(value)

    def write_domain(self, domain):
        """
        Write the domain to the stream.
        """
        self.stream.write('M(D) = {')
        self.stream.write(', '.join('d' + str(id) for id in domain))
        self.stream.write('}')

    def write_constant(self, constant, identifier):
        """
        Write a single constant to the stream.
        """
        self.stream.write('M({}) = d{}'.format(constant, identifier))

    def write_predicate(self, name, extension):
        """
        Write a predicate to the stream.
        """
        self.stream.write('M({}) = {{'.format(name))
        self.stream.write(', '.join(make_pair(('d' + str(id) for id in pair), '<', '>')
                                    for pair in extension))
        self.stream.write('}')
