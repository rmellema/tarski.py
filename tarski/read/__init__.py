"""
This module is for reading in the formal structures in different formats. This is done by defining
an abstract base class for Readers, which can then be implemented by Readers for specific file
formats.

Currently only Tarski's World is supported.
"""
__all__ = ['tarski']

from abc import ABC, abstractmethod
import sys

class AbstractWorldReader(ABC):
    """
    The abstract class that defines the interface in use for `Reader`s.
     .. py:attribute:: format_name

        The name of the format as a string. Must be overridden by implementations and have a maximum
        length of 20.

    .. py:attribute:: format_description

        A short description of this format as a string. Must be overridden by implementations and
        have a maximum length of 60.
    """
    def __init__(self, stream=sys.stdin):
        """
        :param stream: The stream to read from. Can be any object that has readline implemented.
        """
        self.stream = stream

    @abstractmethod
    def read_world(self):
        """
        A method that reads in a world from the stream. Must be overridden by implementations.

        :raises ReaderException: When an exception occurs during reading
        :returns: The next world from the stream.
        :rtype: World
        """

class ReaderException(Exception):
    """
    An exception that can be raised by object implementing :py:class:`AbstractWorldReader` when an
    exception happens during reading.
    """
