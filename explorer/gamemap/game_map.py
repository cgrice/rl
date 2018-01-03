from random import randint, choice

from ecs import Entity
from ecs.components import Physical, Appearance, Position
from explorer.gamemap.tile import Tile
from explorer.gamemap.themes.dungeon import STANDARD_DUNGEON

FOV_ALGO = 'SHADOW'  #default FOV algorithm
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10

class GameMap:

    def __init__(self, width, height, stageIndex = -1, theme = None):
        self.width = width
        self.height = height

        self.theme = STANDARD_DUNGEON
        if theme != None:
            self.theme = theme

        self.ground_color = self.theme['ground-color']
        self.wall_color = self.theme['wall-color']

        self.tiles = [[ set()
        for y in range(self.height) ]
            for x in range(self.width) ]
        self.blocked = [[ set()
        for y in range(self.height) ]
            for x in range(self.width) ]
        self.visible_tiles = []
        
        self.noFOW = False
        self.stageIndex = stageIndex

    def addEntity(self, entity, x, y):
        self.tiles[x][y].add(entity)

    def removeEntity(self, entity, x, y):
        self.tiles[x][y].remove(entity)

    def in_bounds(self, x, y):
        return (x < self.width and x > 0 and y < self.height and y > 0)

    def is_blocked(self, x, y):
        if x >= self.width or x < 0:
            return False
        elif y >= self.height or y < 0:
            return False

        try:
            for entity in self.tiles[x][y]:
                physical = entity.getComponent('physical')

                if physical == False:
                    continue

                blocked = physical.blocked
                # blocks_sight = physical.blocks_sight
                if blocked:
                    return True
            return False
        except:
            return True

    def is_visible(self, x, y):
        if x >= self.width or x < 0:
            return False
        elif y >= self.height or y < 0:
            return False

        try:
            for entity in self.tiles[x][y]:
                physical = entity.getComponent('physical')

                if physical == False:
                    continue

                blocks_sight = physical.blocks_sight
                if blocks_sight:
                    return False
            return True
        except:
            return False

    def createWall(self, x, y):
        color = self.wall_color
        # color = (100, 0, 0, 0)
        # modifier = randint(-10, 10)
        # color = (
        #     color[0],
        #     color[1] + modifier,
        #     color[2] + modifier,
        #     color[3] + modifier,
        # )
        wallTile = choice(self.theme['tiles']['wall'])
        wall = Entity()
        wall.addComponent('position', Position(x=x, y=y, stage=self.stageIndex))
        wall.addComponent('appearance', Appearance('wall', character=wallTile, bgcolor=color, fgcolor=(255,255,255,255), layer=0))
        wall.addComponent('physical', Physical(blocks_sight = True, blocked = True))
        return wall

    def createFloor(self, x, y):
        color = self.ground_color
        # color = (100, 0, 0, 0)
        # modifier = randint(0, 6)
        # color = (
        #     color[0],
        #     color[1] + modifier,
        #     color[2] + modifier,
        #     color[3] + modifier,
        # )
        floorTile = choice(self.theme['tiles']['ground'])
        floor = Entity()
        floor.addComponent('position', Position(x=x, y=y, stage=self.stageIndex))
        floor.addComponent('appearance', Appearance('floor', character=floorTile, bgcolor=color, fgcolor=(255,255,255,255), layer=0))
        floor.addComponent('physical', Physical(blocks_sight = False, blocked = False))
        return floor

    def createDoor(self, x, y):
        color = self.ground_color
        door = Entity()
        door.addComponent('position', Position(x=x, y=y, stage=self.stageIndex))
        door.addComponent('appearance', Appearance('door', character=0xE021, bgcolor=color, fgcolor=(255,255,255,255), layer=1))
        door.addComponent('physical', Physical(blocks_sight = True, blocked = True))
        return door

    def getEntities(self):
        tiles = []
        for y in range(self.height):
            for x in range(self.width):
                for entity in self.tiles[x][y]:
                    tiles.append(entity)
                
        return tiles

    def __getitem__(self, key):
        return self.tiles[key]