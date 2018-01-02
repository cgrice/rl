class LocationManager(object):

    def __init__(self):
        self.map = {}
        self.currentStage = -1
        self.entities = {}

    def add(self, entity):
        position = entity.getComponent('position')
        if position != False:
            if position.stage not in self.map:
                self.map[position.stage] = {}
            if position.x not in self.map[position.stage]:
                self.map[position.stage][position.x] = {}
            if position.y not in self.map[position.stage][position.x]:
                self.map[position.stage][position.x][position.y] = set()

            self.map[position.stage][position.x][position.y].add(entity)
            self.entities[entity.uid] = (position.stage, position.x, position.y)

    def update(self, entity, x, y):
        position = entity.getComponent('position')

        try:
            currentStage, currentX, currentY = self.entities[entity.uid]
            self.map[currentStage][currentX][currentY].remove(entity)
        except: 
            pass

        position.x = x
        position.y = y

        entity.addComponent('position', position)
        self.map[position.stage][x][y].add(entity)


        

    def get(self, stage, x, y):
        return self.map[stage][x][y]

    # def remove(self, stage, x, y):
    #     self.map[stage][x][y].

    def setStage(self, stage):
        self.currentStage = stage

    def is_visible(self, x, y):
        return self.is_blocked(self.currentStage, x, y)

    def is_blocked(self, stage, x, y):
        try:
            for entity in self.map[stage][x][y]:
                physical = entity.getComponent('physical')

                if physical == False:
                    continue

                blocked = physical.blocked
                blocks_sight = physical.blocks_sight
                if blocked and blocks_sight:
                    return True
            return False
        except Exception as e:
            # raise e
            return True

