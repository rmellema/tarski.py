"""
A collection of utility functions for writing the models.
"""

def make_pair(coll, lbracket='<', rbracket='>'):
    """
    A context aware function for making a string representation of elements of relationships.
    It takes into account the length of the element. If there is just one element, the brackets are
    left of, but when there are more, all the elements will be seperated by a comma, and the
    brackets will be inserted as well.

    :param coll: The collection that needs to be printed. Can be a generator, but cannot be
                 infinite.
    :param str lbracket: The bracket that goes on the left.
    :param str rbracket: The bracket that goes on the right.
    :returns: A context aware string representation of the pair.
    :rtype: str
    """
    coll = list(coll)
    if len(coll) == 1:
        return str(coll[0])
    return lbracket + ', '.join(coll) + rbracket
