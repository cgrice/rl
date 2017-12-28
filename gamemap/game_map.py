import tdl
from ecs import Entity
from ecs.components import Physical, Appearance, Position
from .tile import Tile

FOV_ALGO = 'SHADOW'  #default FOV algorithm
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10

color_dark_wall = (75, 75, 90)
color_dark_ground = (30, 30, 40)
color_dark_door = (130, 85, 50)
color_light_door = (130, 85, 50)
color_light_wall = (200, 200, 200)
color_light_ground = (148, 148, 148)

class GameMap:

    def __init__(self, width, height, stageIndex = -1):
        self.width = width
        self.height = height

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
        wall = Entity()
        wall.addComponent('position', Position(x=x, y=y, stage=self.stageIndex))
        wall.addComponent('appearance', Appearance('wall', bgcolor=color_dark_wall, layer=0))
        wall.addComponent('physical', Physical(blocks_sight = True, blocked = True))
        return wall

    def createFloor(self, x, y):
        floor = Entity()
        floor.addComponent('position', Position(x=x, y=y, stage=self.stageIndex))
        floor.addComponent('appearance', Appearance('floor', bgcolor=color_dark_ground, layer=0))
        floor.addComponent('physical', Physical(blocks_sight = False, blocked = False))
        return floor

    def createDoor(self, x, y):
        door = Entity()
        door.addComponent('position', Position(x=x, y=y, stage=self.stageIndex))
        door.addComponent('appearance', Appearance('door', bgcolor=color_dark_door, layer=0))
        door.addComponent('physical', Physical(blocks_sight = True, blocked = True))
        return door

   

    def getEntities(self):
        tiles = []
        for y in range(self.height):
            for x in range(self.width):
                tiles.append(self.tiles[x][y])
                
        return tiles

    def computeFOV(self, playerX, playerY):
        self.visible_tiles = tdl.map.quickFOV(
            playerX, playerY, self.is_visible,
            fov=FOV_ALGO,
            radius=TORCH_RADIUS,
            lightWalls=FOV_LIGHT_WALLS
        )

    def __getitem__(self, key):
        return self.tiles[key]