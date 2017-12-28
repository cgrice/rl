from ecs import Entity

class Engine(object):
    '''A game engine to hold state about entities and componenets within
    a game system.

    >>> e = Engine()
    >>> p = Entity(1)
    >>> e.addEntity(p)
    >>> e.entities[1].uid
    1
    >>> e.addComponentToEntity(1, 'test', 'bar')
    >>> entities = e.getEntitiesWithComponents('test')
    >>> entities[0].uid
    1
    >>> e.entities[1].hasComponent('test')
    True
    '''

    def __init__(self):
        self.entities = {}
        self.componentMap = {}
        self.stages = {}
        self.stageIndex = -1

    def addStage(self, index, gamemap):
        gamemap.stageIndex = index
        self.stages[index] = gamemap

    def hasStage(self, index):
        return index in self.stages

    def setStage(self, index):
        if self.stageIndex in self.stages:
            for entity in self.stages[self.stageIndex].getEntities():
                self.removeEntity(entity)
        self.stageIndex = index
        for entity in self.stages[index].getEntities():
            self.addEntity(entity)
        
    def getStage(self):
        return self.stages[self.stageIndex]

    def addEntity(self, entity):
        self.entities[entity.uid] = entity
        self._addEntityComponents(entity)
    
    def removeEntity(self, entity):
        self.entities.pop(entity.uid)
        self._removeEntityComponents(entity)
        
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

    def getEntity(self, uid):
        return self.entities[uid]

    def getEntitiesWithComponents(self, *components):
        hashkey = self._hash(components)
        uids = self.componentMap[hashkey]
        return [self.getEntity(uid) for uid in uids]


    def updateComponent(self, uid, name, component):
        self.entities[uid].addComponent(name, component)

    def addComponentToEntity(self, uid, name, component):
        entity = self.getEntity(uid)
        entity.addComponent(name, component)
        self.entities[uid] = entity
        self._addEntityComponents(entity)

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


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())