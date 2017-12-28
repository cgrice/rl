class LightSource(object):

    def __init__(self, strength = 3, radius = 10, tint = False):
        self.radius = radius
        self.tint = tint
        self.strength = strength