class Physical(object):

    def __init__(self, blocks_sight = False, blocked = True, explored = False, visible = False):
        self.blocks_sight = blocks_sight
        self.blocked = blocked
        self.explored = explored
        self.visible = visible