from .tile import Tile

class GameMap:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.tiles = [[ Tile(False)
        for y in range(self.height) ]
            for x in range(self.width) ]

    def in_bounds(self, x, y):
        return (x < self.width and x > 0 and y < self.height and y > 0)

    def is_blocked(self, x, y):
        try:
            blocked = self.tiles[x][y].blocked
            blocks_sight = self.tiles[x][y].blocks_sight
            return blocked and blocks_sight
        except:
            return True

    def __getitem__(self, key):
        return self.tiles[key]