import uuid

class Entity(object):
    '''A container for an ID that is used in the game world
    
    An entity has a relationship to a number of components

    >>> e = Entity(1)
    >>> print(e.uid)
    1
    >>> e.addComponent('health', {'foo': 'bar'})
    >>> e.hasComponent('health')
    True
    >>> e.addComponent('position', {})
    >>> e.hasComponents('health', 'position')
    True
    >>> e.hasComponents('health', 'missing')
    False
    >>> e.getComponent('health')
    {'foo': 'bar'}
    >>> e.getComponent('missing')
    False
    >>> e.removeComponent('health')
    >>> e.hasComponent('health')
    False
    '''

    def __init__(self, uid = None):
        self.uid = uuid.uuid4 if uid is None else uid
        self.components = {}

    def addComponent(self, name, component):
        self.components[name] = component

    def hasComponent(self, name):
        return name in self.components

    def hasComponents(self, *names):
        for name in names:
            if self.hasComponent(name) == False:
                return False
        return True

    def getComponent(self, name):
        if self.hasComponent(name):
            return self.components[name]
        return False

    def removeComponent(self, name):
        self.components.pop(name)


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())