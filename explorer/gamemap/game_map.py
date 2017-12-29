from random import randint

from ecs import Entity
from ecs.components import Physical, Appearance, Position
from explorer.gamemap.tile import Tile

FOV_ALGO = 'SHADOW'  #default FOV algorithm
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10

class GameMap:

    def __init__(self, width, height, stageIndex = -1):
        self.width = width
        self.height = height

        self.ground_color = (48, 43, 26)
        self.wall_color =  (85, 85, 85)

        self.tiles = [[ Tile(False)
        for y in range(self.height) ]
            for x in range(self.width) ]
        self.blocked = [[ Tile(False)
        for y in range(self.height) ]
            for x in range(self.width) ]
        self.visible_tiles = []
        
        self.noFOW = False
        self.stageIndex = stageIndex

    def in_bounds(self, x, y):
        return (x < self.width and x > 0 and y < self.height and y > 0)

    def is_blocked(self, x, y):
        try:
            physical = self.tiles[x][y].getComponent('physical')
            blocked = physical.blocked
            blocks_sight = physical.blocks_sight
            return blocked and blocks_sight
        except:
            return True

    def is_visible(self, x, y):
        if x >= self.width or x < 0:
            return False
        elif y >= self.height or y < 0:
            return False
        elif self.is_blocked(x, y) == True:
            return False
        else:
            return True

    def createWall(self, x, y):
        color = self.wall_color
        modifier = randint(-10, 10)
        color = (
            color[0] + modifier,
            color[1] + modifier,
            color[2] + modifier,
        )
        
        wall = Entity()
        wall.addComponent('position', Position(x=x, y=y, stage=self.stageIndex))
        wall.addComponent('appearance', Appearance('wall', bgcolor=color, layer=0))
        wall.addComponent('physical', Physical(blocks_sight = True, blocked = True))
        return wall

    def createFloor(self, x, y):
        color = self.ground_color
        modifier = randint(0, 6)
        color = (
            color[0] + modifier,
            color[1] + modifier,
            color[2] + modifier
        )
        floor = Entity()
        floor.addComponent('position', Position(x=x, y=y, stage=self.stageIndex))
        floor.addComponent('appearance', Appearance('floor', bgcolor=color, layer=0))
        floor.addComponent('physical', Physical(blocks_sight = False, blocked = False))
        return floor

    # def createDoor(self, x, y):
    #     door = Entity()
    #     door.addComponent('position', Position(x=x, y=y, stage=self.stageIndex))
    #     door.addComponent('appearance', Appearance('door', bgcolor=color_dark_door, layer=0))
    #     door.addComponent('physical', Physical(blocks_sight = True, blocked = True))
    #     return door

    def getEntities(self):
        tiles = []
        for y in range(self.height):
            for x in range(self.width):
                tiles.append(self.tiles[x][y])
                
        return tiles

    def __getitem__(self, key):
        return self.tiles[key]