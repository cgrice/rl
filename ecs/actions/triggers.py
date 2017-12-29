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
            y = y + 1
        else:
            x, y = stage.exit
            y = y - 1

        position.x = x
        position.y = y
        target.addComponent('position', position)
        appearance = target.getComponent('appearance')
        
        self.engine.addMessage(
            '%s is now in floor %s' % (appearance.name, nextIndex), 
            (255,200,200)
        )