"""
This module allows for the reading of Tarski's world files and transforming them into the
corresponding formal structures.
"""
from . import AbstractWorldReader, ReaderException
from ..world import World, Shape, Size

class TarskiWorldReader(AbstractWorldReader):
    """
    A reader for reading in Tarski's World files.
    """
    def format_name(self):
        "The name of the format. Required by ABC"
        return "tarski"

    def format_description(self):
        "A short description of the format. Required by ABC"
        return "The file format in use by Tarski's World."

    def skip_header(self):
        """
        Skip enough lines in the file to find the actual number of blocks in this file.

        :raises ReaderException: If the Wld Type is not known
        :returns: The number of blocks in this file
        :rtype: int
        """
        self.stream.readline()
        self.stream.readline()
        wld = self.stream.readline().strip()
        if wld[-1] == 'P': # Version 6, probably
            return int(self.stream.readline().strip())
        elif wld[-1] == 'F': # Version 7, probably
            self.stream.readline()
            self.stream.readline()
            return int(self.stream.readline().strip())
        else:
            raise ReaderException("Unrecognized Wld Type: '{}'".format(wld[-1]))

    def read_numbers(self):
        """
        Read the two numbers that are on the next line, and return them as a tuple.

        :returns: A tuple with the numbers on the next line.
        :rtype: tuple(int, int)
        """
        line = self.stream.readline().strip().split(' ')
        return (int(line[0]), int(line[1]))

    def read_block(self):
        """
        Read the next block from the stream.

        :raises ReaderException: If the block name is not given.
        :returns: The information for the next block, as a tuple
        :rtype: tuple(Shape, Size, int, int, str)
        """
        shape_num, size_num = self.read_numbers()
        x, y = self.read_numbers()
        name = self.stream.readline().strip()
        if name[0] != "'":
            raise ReaderException("Expected name, found: '{}'".format(name[0]))
        return (Shape(shape_num), Size(size_num), x, y, name[1:])

    def read_world(self, world=None):
        """
        Read in a world from the stream. You can also use this to read new blocks into an already
        existing world.

        :param World world: The world to read into. Ignored if not given.
        :returns: The new world
        :rtype: World
        """
        if not world:
            world = World()
        num_blocks = self.skip_header()
        for _ in range(num_blocks):
            shape, size, x, y, name = self.read_block()
            block = world.add_block(size, shape, (x, y))
            if name:
                world.add_constant(name, block)
        self.stream.readline()
        return world
