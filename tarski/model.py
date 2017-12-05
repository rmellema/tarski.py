"""
A module for representing the actual first-order structure of a Block World. The structure can
either be made from a World, or be made by hand.
"""

class Model:
    """
    The model that represents the first-order structure.
    """
    def __init__(self, *, world=None):
        self._last_entity = 0
        self.domain = set()
        self.constants = dict()
        self.predicates = dict()
        if world:
            self._from_world(world)

    def __str__(self):
        return "#<model domain: {} constants: {} {} predicates>".format(self.domain,
                                                                        self.constants,
                                                                        len(self.predicates.keys()))

    def _add_unary_predicates(self, world):
        """
        Add all the information about the unary predicates from `world` to this model.
        """
        self.add_predicate("Tet")
        self.add_predicate("Cube")
        self.add_predicate("Dodec")
        self.add_predicate("Small")
        self.add_predicate("Medium")
        self.add_predicate("Large")
        for block in world.domain:
            if block.is_tetrahedron():
                self.add_to_extension("Tet", [block.identifier])
            if block.is_cube():
                self.add_to_extension("Cube", [block.identifier])
            if block.is_dodecahedron():
                self.add_to_extension("Dodec", [block.identifier])
            if block.is_small():
                self.add_to_extension("Small", [block.identifier])
            if block.is_medium():
                self.add_to_extension("Medium", [block.identifier])
            if block.is_large():
                self.add_to_extension("Large", [block.identifier])

    def _add_binary_predicates(self, world):
        """
        Add all the information about the binary predicates from `world` to this model.
        """
        # pylint: disable=too-many-branches
        self.add_predicate("SameSize")
        self.add_predicate("SameShape")
        self.add_predicate("Larger")
        self.add_predicate("Smaller")
        self.add_predicate("SameCol")
        self.add_predicate("SameRow")
        self.add_predicate("Adjoins")
        self.add_predicate("LeftOf")
        self.add_predicate("RightOf")
        self.add_predicate("FrontOf")
        self.add_predicate("BackOf")
        for block in world.domain:
            for other in world.domain:
                if block.is_same_size(other):
                    self.add_to_extension("SameSize", [block.identifier, other.identifier])
                if block.is_same_shape(other):
                    self.add_to_extension("SameShape", [block.identifier, other.identifier])
                if block != other:
                    if block.is_smaller(other):
                        self.add_to_extension("Smaller", [block.identifier, other.identifier])
                    if block.is_larger(other):
                        self.add_to_extension("Larger", [block.identifier, other.identifier])
                    if block.in_same_column(other):
                        self.add_to_extension("SameCol", [block.identifier, other.identifier])
                    if block.in_same_row(other):
                        self.add_to_extension("SameRow", [block.identifier, other.identifier])
                    if block.does_adjoin(other):
                        self.add_to_extension("Adjoins", [block.identifier, other.identifier])
                    if block.is_left_of(other):
                        self.add_to_extension("LeftOf", [block.identifier, other.identifier])
                    if block.is_right_of(other):
                        self.add_to_extension("RightOf", [block.identifier, other.identifier])
                    if block.is_front_of(other):
                        self.add_to_extension("FrontOf", [block.identifier, other.identifier])
                    if block.is_back_of(other):
                        self.add_to_extension("BackOf", [block.identifier, other.identifier])

    def _add_trinary_predicates(self, world):
        """
        Add all the trinary predicates from `world` to the model.
        """
        self.add_predicate("Between")
        for block in world.domain:
            for first in world.domain:
                if block == first:
                    continue
                for second in world.domain:
                    if block == second or first == second:
                        continue
                    if first.in_between(first, second):
                        self.add_to_extension("Between", [block.identifier, first.identifier,
                                                          second.identifier])
                        # If a block is between a and b, then it is also between b and a
                        self.add_to_extension("Between", [block.identifier, second.identifier,
                                                          first.identifier])

    def _from_world(self, world):
        """
        Create a new model from a World.

        :param World world: The world to create a model from
        :returns: The newly created model.
        """
        for block in world.domain:
            self.add_entity(block.identifier)
        for constant in world.all_constants():
            block = world.get_constant(constant)
            self.add_constant(constant, block.identifier)
        # Adding the predicates #
        self._add_unary_predicates(world)
        self._add_binary_predicates(world)
        self._add_trinary_predicates(world)

    def add_entity(self, entity=None):
        """
        Add a new entity to the model. If no entity is specified a new one will be generated.

        :param entity: The entity to add. If None, a new entity will be made.
        :returns: The new entity added.
        """
        if entity is None:
            self._last_entity += 1
            entity = self._last_entity
        self.domain.add(entity)
        return entity

    def add_constant(self, constant, entity):
        """
        Add a (new) name for an already existing entity.

        :param str constant: The name
        :param entity: The entity for which to add the name
        :raises ValueError: If the entity is not already in the model.
        """
        if entity not in self.domain:
            raise ValueError("The given entity is not in the domain")
        self.constants[constant] = entity

    def add_predicate(self, name):
        """
        Add a predicate with `name`.

        :param str name: The name of the new predicate. Will be Sentence cased if it is not already.
        """
        name = name[0].upper() + name[1:]
        if name not in self.predicates:
            self.predicates[name] = set()

    def add_to_extension(self, predicate, entities):
        """
        Add all the `entities` to the extension of `predicate`.

        :param str predicate: A predicate in the Model.
        :param entities: The entities to be added to the extension.
        """
        if predicate not in self.predicates:
            raise ValueError("No predicate named: '{}'".format(predicate))
        for entity in entities:
            if entity not in self.domain:
                raise ValueError("Entity '{}' not in model".format(entity))
        self.predicates[predicate].add(tuple(entities))
