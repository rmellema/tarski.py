"""
A module for representing the actual first-order structure of a Block World. The structure can
either be made from a World, or be made by hand.
"""

class Model:
    """
    The model that represents the first-order structure.
    """
    def __init__(self):
        self._last_entity = 0
        self.domain = set()
        self.constants = dict()
        self.predicates = dict()

    def __str__(self):
        ret = []
        ret.append('M(D) = {' + ', '.join('d{}'.format(id) for id in self.domain) + '}')
        ret.extend('M({}) = d{}'.format(constant, entity)
                   for constant, entity in self.constants.items())
        ret.extend('M({}) = {{'.format(predicate) +
                   ','.join('<' + ', '.join('b{}'.format(id) for id in entities) + '>'
                            for entities in extension) + '}'
                   for predicate, extension in self.predicates.items())
        return '\n'.join(ret)

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

    @classmethod
    def from_world(cls, world):
        """
        Create a new model from a World.

        :param World world: The world to create a model from
        :returns: The newly created model.
        """
        model = cls()
        for block in world.domain:
            model.add_entity(block.identifier)
        for constant in world.all_constants():
            block = world.get_constant(constant)
            model.add_constant(constant, block.identifier)
        # Adding the predicates #
        model._add_unary_predicates(world)
        model._add_binary_predicates(world)
        return model

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
