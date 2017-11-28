"""
This module allows for the reading of Tarski's world files and transforming them into the
corresponding formal structures.
"""
from ..world import World, Shape, Size

class ReadError(Exception):
    """
    An exception that is throw whenever the Reader finds something that it does not expect.
    """
    pass

def skip_header(filestream):
    """
    Skip enough lines in the file to find the actual number of blocks in this file.

    :param file filestream: The filestream to read from. The header should still be intact
    :returns: The number of blocks in this file
    :rtype: int
    """
    filestream.readline()
    filestream.readline()
    wld = filestream.readline().strip()
    if wld[-1] == 'P': # Version 6, probably
        return int(filestream.readline().strip())
    elif wld[-1] == 'F': # Version 7, probably
        filestream.readline()
        filestream.readline()
        return int(filestream.readline().strip())
    else:
        raise ReadError("Unrecognized Wld Type: '{}'".format(wld[-1]))

def read_numbers(filestream):
    """
    Read the two numbers that are on the next line, and return them as a tuple.

    :param file filestream: The Stream to read from.
    :returns: A tuple with the numbers on the next line.
    :rtype: tuple(int, int)
    """
    line = filestream.readline().strip().split(' ')
    return (int(line[0]), int(line[1]))

def read_block(filestream):
    """
    Read the next block from the stream.

    :param file filestream: The stream to read from.
    :returns: The information for the next block, as a tuple
    :rtype: tuple(Shape, Size, int, int, str)
    """
    shape_num, size_num = read_numbers(filestream)
    x, y = read_numbers(filestream)
    name = filestream.readline().strip()
    if name[0] != "'":
        raise ReadError("Expected name, found: '{}'".format(name[0]))
    return (Shape(shape_num), Size(size_num), x, y, name[1:])

def read_file(filestream, world=None):
    """
    From a given file, read in all the blocks and add them to `world`. If `world` is not given, a
    new world is created for you.

    :param file filestream: The object from which to read the world. Can be any subclass from
                            IOBase.
    :param World world: The world to read into. Defaults to the empty world
    :returns: The new world
    :rtype: World
    """
    if not world:
        world = World()
    num_blocks = skip_header(filestream)
    for _ in range(num_blocks):
        shape, size, x, y, name = read_block(filestream)
        block = world.add_block(size, shape, (x, y))
        if name:
            world.add_constant(name, block)
    filestream.readline()
    return world
