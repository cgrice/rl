class MoveStage(object):

    def __init__(self, engine, direction = 1):
        self.engine = engine
        self.direction = direction

    def __call__(self, source, target):
        nextIndex = self.engine.stageIndex + self.direction
        self.engine.setStage(nextIndex)
        stage = self.engine.getStage()
        position = target.getComponent('position')
        position.stage = nextIndex

        if self.direction > 0:
            x, y = stage.start
            x = x + 1
        else:
            x, y = stage.exit
            x = x - 1

        position.x = x
        position.y = y
        target.addComponent('position', position)
        appearance = target.getComponent('appearance')
        
        self.engine.addMessage(
            '%s is now in floor %s' % (appearance.name, nextIndex), 
            (255,255,200,200)
        )

class LogMessage(object):

    def __init__(self, engine, message = ''):
        self.message = message
        self.engine = engine

    def __call__(self, source, target):
        appearance = target.getComponent('appearance')
        message = '%s %s' % (appearance.name, self.message)
        self.engine.addMessage(message, (255, 255, 200, 200))

class AddToInventory(object):

    def __init__(self, engine):
        self.engine = engine

    def __call__(self, source, target):
        inventory = target.getComponent('inventory')

        if inventory:
            inventory.addItem(source.uid)
        
        em = self.engine.entityManager
        em.removeEntity(source)
        source.removeComponent('physical')
        source.removeComponent('position')
        source.removeComponent('trigger')
        em.addEntity(source)