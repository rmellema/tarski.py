"""
This module is for writing the formal structure or the block world in different formats. This is
done by defining abstract base classes for Writers, which can then be implemented by Writers for
specific formats.

If you want to support additional formats, you can use the `tarski.writers` entry point in your
`setup.py`.
"""

from abc import ABC, abstractmethod
import sys

class AbstractModelWriter(ABC):
    """
    The abstract class that defines the interface in use for `Writer` s.

    .. py:attribute:: format_name

        The name of the output format as a string. Must be overridden by implementations and has a
        maximum length of 20.

    .. py:attribute:: format_description

        A short description of this output format as a string. Must be overridden by implementations
        and have a maximum lenght of 60.
    """
    def __init__(self, stream=sys.stdout):
        """
        :param stream: The stream to write to. Can be any object that has `write` implemented.
        """
        self.stream = stream

    @abstractmethod
    def write_domain(self, domain):
        """
        Write the domain of the model. Must be overwritten by implementations.

        :param domain: The domain to write.
        """

    @abstractmethod
    def write_constant(self, constant, identifier):
        """
        Write a single constant to the stream. Must be overwritten by implementations.

        :param str constant: The name of the constant to write.
        :param identifier: The value of the constant.
        """

    def write_constants(self, constants):
        """
        Write all the constant from the model on their own line in order of appereance. Can be
        overwritten if the implementation needs a special behaviour.

        :param constants: The constants to write
        :type constants: dict[str, Block]
        """
        for constant, entity in constants.items():
            self.write_constant(constant, entity)
            self.stream.write('\n')

    @abstractmethod
    def write_predicate(self, name, extension):
        """
        Write a predicate and its extension to the stream. Must be overwritten by definitions

        :param str name: The name of this predicate.
        :param tuple[Block] extension: The set which defines this predicate.
        """

    def write_predicates(self, predicates):
        """
        Write all the predicates in `predicates` to the stream on their own line in order of
        appereance. Can be overwritten of other behaviour is required.

        :param predicates: The predicates to write to the stream.
        :type predicates: dict[str, tuple[Block]]
        """
        for predicate, extension in predicates.items():
            self.write_predicate(predicate, extension)
            self.stream.write('\n')

    def write_model(self, model):
        """
        Write the model to the stream. By default, it first writes the domain, then the constants,
        and it ends with the predicates. Can be overwritten if an other order is prefered.

        :param Model model: The model to write to the stream.
        """
        self.write_domain(model.domain)
        self.stream.write('\n')
        self.write_constants(model.constants)
        self.write_predicates(model.predicates)
