class Appearance(object):

    def __init__(self, name, 
        bgcolor = None, 
        fgcolor = None, 
        character = ' ', 
        layer = 0,
        lighting = False
    ):
        self.name = name
        self.fgcolor = fgcolor
        self.bgcolor = bgcolor
        self.character = character
        self.layer = layer
        self.lighting = lighting