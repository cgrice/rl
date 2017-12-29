class Tile:

    def __init__(self, blocked = False, block_sight = False):
        self.blocked = blocked
        if block_sight is None: 
            block_sight = blocked
        self.block_sight = block_sight
        self.color = None
        self.visible = False
        self.explored = False