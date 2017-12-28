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
    >>> e.componentMap['test']
    {1}
    >>> e.entities[1].hasComponent('test')
    True
    >>> entities = e.getEntitiesWithComponents('test')
    >>> entities[0].uid
    1
    '''

    def __init__(self):
        self.entities = {}
        self.componentMap = {}


    def addEntity(self, entity):
        self.entities[entity.uid] = entity

    def getEntity(self, uid):
        return self.entities[uid]

    def getEntitiesWithComponents(self, *components):
        sets = []
        for c in components:
            sets.append(self.componentMap[c])
        
        uids = set.intersection(*sets)
        
        return [self.getEntity(uid) for uid in uids]


    def addComponentToEntity(self, uid, name, component):
        if name not in self.componentMap:
            self.componentMap[name] = set()

        self.entities[uid].addComponent(name, component)
        self.componentMap[name].add(uid)


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())