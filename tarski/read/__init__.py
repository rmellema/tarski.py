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
    """
    def __init__(self, stream=sys.stdin):
        """
        :param stream: The stream to read from. Can be any object that has readline implemented.
        """
        self.stream = stream

    @property
    @abstractmethod
    def format_name(self):
        """
        The name of the format as a string. Must be overridden by implementations.
        """

    @property
    @abstractmethod
    def format_description(self):
        """
        A short description of this format as a string. Must be overridden by implementations.
        """

    @abstractmethod
    def read_world(self):
        """
        A method that reads in a world from the stream. Must be overridden by implementations.

        :raises ReaderException: When an exception occurs during reading
        :returns: The next world from the stream.
        :rtype: World
        """

def ReaderException(Exception):
    """
    An exception that can be raised by object implementing :py:class:`AbstractWorldReader` when an
    exception happens during reading.
    """
