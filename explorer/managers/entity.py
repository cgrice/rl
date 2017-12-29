class EntityManager(object):
    '''A game engine to hold state about entities and componenets within
    a game system.

    >>> from ecs import Entity
    >>> e = Engine()
    >>> p = Entity(1)
    >>> e.addEntity(p)
    >>> e.entities[1].uid
    1
    >>> p.addComponent('test', 'bar')
    >>> entities = e.getEntitiesWithComponents('test')
    >>> entities[0].uid
    1
    >>> e.entities[1].hasComponent('test')
    True
    '''

    def __init__(self):
        self.entities = {}
        self.componentMap = {}

    def addEntity(self, entity):
        self.entities[entity.uid] = entity
        self._addEntityComponents(entity)
    
    def removeEntity(self, entity):
        self.entities.pop(entity.uid)
        self._removeEntityComponents(entity)

    def getEntity(self, uid):
        return self.entities[uid]
        
    def _removeEntityComponents(self, entity):
        for hashkey in list(self.componentMap):
            try:
                self.componentMap[hashkey].remove(entity.uid)
            except:
                pass

    def _addEntityComponents(self, entity):
        components = entity.getComponentNames()
        for combination in self._powerset(components):
            hashed = self._hash(combination)
            if hashed not in self.componentMap:
                self.componentMap[hashed] = set()
            self.componentMap[hashed].add(entity.uid)

    def getEntitiesWithComponents(self, *components):
        hashkey = self._hash(components)
        try:
            uids = self.componentMap[hashkey]
        except:
            raise KeyError('There are no entities with the components: {0}'.format(components))
        return [self.getEntity(uid) for uid in uids]

    def _powerset(self, components):
        """
        Returns all the subsets of this set. This is a generator.
        """
        if len(components) <= 1:
            yield components
            yield []
        else:
            for item in self._powerset(components[1:]):
                yield [components[0]]+item
                yield item

    def _hash(self, components):
        return hash(frozenset(components))
