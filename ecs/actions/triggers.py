import time

class MoveStage(object):

    def __init__(self, engine, direction = 1):
        self.engine = engine
        self.direction = direction

    def __call__(self, source, target):
        position = target.getComponent('position')
        nextIndex = self.engine.stageIndex + self.direction
        position.stage = nextIndex

        self.engine.getStage().removeEntity(target, position.x, position.y)
        self.engine.setStage(nextIndex)
        stage = self.engine.getStage()

        if self.direction > 0:
            x, y = stage.start
            x = x + 1
        else:
            x, y = stage.exit
            x = x - 1

        position.x = x
        position.y = y
        target.addComponent('position', position)
        self.engine.getStage().addEntity(target, position.x, position.y)
        self.engine.camera.move(position.x, position.y, stage)
        
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
        self.engine.addMessage(message, (255, 100, 100, 0))

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

class ShowDialogue(object):

    def __init__(self, engine):
        self.engine = engine

    def __call__(self, source, target):
        dialogue = source.getComponent('dialogue')
        position = source.getComponent('position')
        self.engine.gui.showInteractions(source, x=position.x, y=position.y)

        # if dialogue != False:
        #     welcome = dialogue.welcome

class ResetInteractions(object):

    def __call__(self, source, target):
        interactable = source.getComponent('interactable')
        interactable.interacted = False
        source.addComponent('interactable', interactable)