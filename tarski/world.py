"""
This module contains all the code for representing the blocks world in Python.
"""
from enum import Enum
from itertools import product
from .util import OrderedEnum

class Shape(Enum):
    """
    Describes the different shapes that an object can have in Tarski's World.
    """
    TETRAHEDRON = 1
    CUBE = 2
    DODECAHEDRON = 3
    TET = TETRAHEDRON
    DODEC = DODECAHEDRON

class Size(OrderedEnum):
    """
    Describes the different sizes that an object can have. They are sorted so "Small" is the
    smallest object.
    """
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

class Block:
    """
    Describes a block in the Block World. It has the following attributes, which all have to be set
    when the block is initialized.

    .. py:attribute:: identifier

        An unique identifier for this block. The creator of the Block must make sure it is
        unique.

    .. py:attribute:: shape

        The shape of this Block.

    .. py:attribute:: size

        The size of this block

    .. py:attribute:: x

        The x location of this block on the board

    .. py:attribute:: y

        The y location of this block on the board
    """
    def __init__(self, identifier, size, shape, x, y):
        self._id = identifier
        self.shape = shape
        self.size = size
        self.x = x
        self.y = y

    def __str__(self):
        "Return a string representation of the Block"
        size = self.size.name.lower()
        shape = self.shape.name.lower()
        return "<Block: {} {}, ({}, {})>".format(size, shape, self.x, self.y)

    @property
    def identifier(self):
        "The id that this block was given. Should be unique for a world."
        return self._id

    def is_tetrahedron(self):
        "Tests if this block is a Tetrahedron"
        return self.shape == Shape.TETRAHEDRON

    def is_cube(self):
        "Tests if this block is a Cube"
        return self.shape == Shape.CUBE

    def is_dodecahedron(self):
        "Tests if this block is a Dodecahedron"
        return self.shape == Shape.DODECAHEDRON

    def is_small(self):
        "Tests if this block is small"
        return self.size == Size.SMALL

    def is_medium(self):
        "Tests if this block is medium"
        return self.size == Size.MEDIUM

    def is_large(self):
        "Tests if this block is medium"
        return self.size == Size.LARGE

    def is_same_size(self, other):
        "Tests if the blocks are the same size"
        return self.size == other.size

    def is_same_shape(self, other):
        "Tests if the blocks are the same shape"
        return self.shape == other.shape

    def is_smaller(self, other):
        """
        Tests if this block is smaller than the `other` block.

        :param Block other: The block to test against.
        """
        return self.size < other.size

    def is_larger(self, other):
        """
        Tests if this block is larger than the `other` block.

        :param Block other: The block to test against.
        """
        return self.size > other.size

    def in_same_column(self, other):
        """
        Tests if this block is in the same column as the other block.

        :param Block other: The block to test against.
        """
        return self.x == other.x

    def in_same_row(self, other):
        """
        Tests if this block is in the same row as the other block.

        :param Block other: The block to test against.
        """
        return self.y == other.y

    def does_adjoin(self, other):
        """
        Tests if this block is next to another block, but not diagonally.

        :param Block other: The block to test against.
        """
        if self.in_same_row(other):
            return abs(self.x - other.x) == 1
        if self.in_same_column(other):
            return abs(self.y - other.y) == 1
        return False

    def is_left_of(self, other):
        """
        Tests if this block is nearer to the left edge of the grid than `other`.

        :param Block other: The block to test against.
        """
        return self.x < other.x

    def is_right_of(self, other):
        """
        Tests if this block is nearer to the right edge of the grid than `other`.

        :param Block other: The block to test against.
        """
        return self.x > other.x

    def is_front_of(self, other):
        """
        Tests if this block is nearer to the front edge of the grid than `other`.

        :param Block other: The block to test against.
        """
        return self.y < other.y

    def is_back_of(self, other):
        """
        Tests if this block is nearer to the back edge of the grid than `other`.

        :param Block other: The block to test against.
        """
        return self.y > other.y

    def in_between(self, first, second):
        """
        Tests if this block lies in between the other two blocks, and if they are all in the same
        row, column, or diagonal.

        :param Block first: The first block for the test
        :param Block second: The second block for the test
        """
        if self.in_same_row(first) and self.in_same_row(second):
            return first.x < self.x < second.x or first.x > self.x > second.x
        if self.in_same_column(first) and self.in_same_column(second):
            return first.y < self.y < second.y or first.y > self.y > second.y
        # Check for the diagonal
        sdc = self.x - self.y
        if (sdc == first.x - first.y) and (sdc == second.x - second.y): # All same diagonal
            return ((first.x < self.x < second.x) or (first.x > self.x > second.x)) and \
                   ((first.y < self.y < second.y) or (first.y > self.y > second.y))
        return False

class World:
    """
    The world that holds all of the actual blocks. It has the following attributes:

    .. py:attribute:: x_size

        The size of the board in the x direction. Has to be set at initialization. Defaults to 8.

    .. py:attribute:: y_size

        The size of the board in the y direction. Has to be set at initialization. Defaults to 8.

    .. py:attribute:: domain

        A set of blocks that symbolize all the blocks that are in this world. It should not be
        directly altered.
    """
    def __init__(self, x_size=8, y_size=8):
        self.x_size = x_size
        self.y_size = y_size
        self._id_counter = 1
        self.domain = set()
        self._constants = {}

    def turn_clockwise(self):
        "Turn this world clockwise by 90 degrees"
        self.x_size, self.y_size = self.y_size, self.x_size
        for block in self.domain:
            block.x, block.y = -block.y + self.x_size - 1, block.x

    def turn_counterclockwise(self):
        "Turn this world counterclockwise by 90 degrees"
        self.x_size, self.y_size = self.y_size, self.x_size
        for block in self.domain:
            block.x, block.y = block.y, -block.x + self.y_size - 1


    def __str__(self):
        "Return a string representation of the world"
        blocks = [str(block) for block in self.domain]
        names = [str((name, str(self.get_constant(name)))) for name in self._constants]
        return "<World: [{}]\n\t[{}]>".format(' '.join(blocks), ' '.join(names))

    def add_constant(self, name, block):
        """
        Assign `name` to `block`, so `name` becomes a constant for `block`. If `name` is already
        a constant, its value gets changed.

        :param str name: The name to assign to `block`.
        :param Block block: The block to assign `name` to.
        """
        self._constants[name] = block

    def get_constant(self, name):
        """
        Get the block bound to `name`, or a KeyError is there is none.

        :param str name: The name for which we want to get the block.
        :return: The block assigned to `name`.
        :rtype: Block
        """
        try:
            return self._constants[name]
        except KeyError:
            raise KeyError("No constant with name '{}'".format(name))

    def remove_constant(self, name):
        """
        Remove the constant `name`, but not the block that it is a name for.

        :param str name: The constant to remove.
        """
        try:
            del self._constants[name]
        except KeyError:
            pass

    def all_constants(self):
        """
        Returns an iterator over all the constants
        """
        return self._constants.keys()

    def add_block(self, size=Size.MEDIUM, shape=Shape.CUBE, loc=None):
        """
        Add a new block to this world.

        :param Size size: The size of the block to add, defaults to Medium.
        :param Shape shape: The shape of the block to add, defaults to Cube.
        :param (int, int) loc: The location of the block as (x, y) coordinates, defaults to the
                                first available position.
        :return: The newly created block
        :rtype: Block
        :raises ValueError: if the x or y of the block is out of range.
        """
        if loc is None:
            locs = [(block.x, block.y) for block in self.domain]
            for y, x in product(range(self.y_size), range(self.x_size)):
                if (x, y) not in locs:
                    loc = (x, y)
                    break
        else:
            if loc[0] >= self.x_size:
                raise ValueError("x value for block out of range")
            if loc[1] >= self.y_size:
                raise ValueError("y value for block out of range")
        block = Block(self._id_counter, size, shape, loc[0], loc[1])
        self.domain.add(block)
        self._id_counter += 1
        return block

    def remove_block(self, block):
        """
        Remove a block from the world. Will also remove any constant names assigned to this block.

        :param block: The block to remove. If it is a string, it is interpreted as a constant name
                        that is bound to a block.
        :type block: Block or str
        """
        constants = []
        if isinstance(block, str):
            constants.append(block)
            block = self.get_constant(block)
        for key, value in self._constants.items():
            if value == block:
                constants.append(key)
        for name in constants:
            self.remove_constant(name)
        try:
            self.domain.remove(block)
        except KeyError:
            pass
