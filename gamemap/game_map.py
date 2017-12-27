import tdl

from .tile import Tile

FOV_ALGO = 'SHADOW'  #default FOV algorithm
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10

color_dark_wall = (50, 50, 150)
color_dark_ground = (40, 40, 80)
color_light_wall = (250, 230, 180)
color_light_ground = (140, 148, 108)

class GameMap:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.tiles = [[ Tile(False)
        for y in range(self.height) ]
            for x in range(self.width) ]
        self.visible_tiles = []

    def in_bounds(self, x, y):
        return (x < self.width and x > 0 and y < self.height and y > 0)

    def is_blocked(self, x, y):
        try:
            blocked = self.tiles[x][y].blocked
            blocks_sight = self.tiles[x][y].blocks_sight
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

    def render(self, console, noFOW = False):
        for y in range(self.height):
            for x in range(self.width):
                console.draw_char(x, y, ' ', bg=(0, 0, 0))
                visible = (x, y) in self.visible_tiles
                wall = self.tiles[x][y].blocks_sight
                if not visible:
                    explored = self.tiles[x][y].explored
                    if explored or noFOW:
                        if wall:
                            console.draw_char(x, y, None, fg=None, bg=color_dark_wall)
                        else:
                            console.draw_char(x, y, None, fg=None, bg=color_dark_ground)
                    continue
                else:
                    if wall:
                        console.draw_char(x, y, None, fg=None, bg=color_light_wall)
                    else:
                        console.draw_char(x, y, None, fg=None, bg=color_light_ground)
                    self.tiles[x][y].explored = True

    def computeFOV(self, playerX, playerY):
        self.visible_tiles = tdl.map.quickFOV(
            playerX, playerY, self.is_visible,
            fov=FOV_ALGO,
            radius=TORCH_RADIUS,
            lightWalls=FOV_LIGHT_WALLS
        )

    def __getitem__(self, key):
        return self.tiles[key]