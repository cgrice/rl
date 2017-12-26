from .tile import Tile

class GameMap:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.tiles = [[ Tile(False)
        for y in range(self.height) ]
            for x in range(self.width) ]

    def is_blocked(self, x, y):
        try:
            blocked = self.tiles[x][y].blocked
            return blocked
        except:
            return True


    def __getitem__(self, key):
        return self.tiles[key]