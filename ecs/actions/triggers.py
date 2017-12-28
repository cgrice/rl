class MoveStage(object):

    def __init__(self, engine, direction = 1):
        self.engine = engine
        self.direction = direction

    def __call__(self, source, target):
        nextIndex = self.engine.stageIndex + self.direction
        self.engine.setStage(nextIndex)
        position = target.getComponent('position')
        position.stage = nextIndex
        target.addComponent('position', position)