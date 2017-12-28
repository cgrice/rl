import tdl

class RenderSystem(object):
    
    def selectRenderable(self, entities):
        return [entity for entity in entities if entity.hasComponents('position', 'appearance', 'physical')]

    def selectPlayer(self, entities):
        return next(entity for entity in entities if entity.hasComponents('player', 'position'))

    def getLayer(self, entity):
        appearance = entity.getComponent('appearance')
        return appearance.layer

    def multiplyColor(self, color, ratio):
        newColor = [0, 0, 0]
        for i, channel in enumerate(color):
            newChannel = int((channel * ratio) // 1)
            if newChannel > 255:
                newChannel = 255
            newColor[i] = newChannel
        return tuple(newColor)

    def tintColor(self, color, tint):
        newColor = [0, 0, 0]
        for i, channel in enumerate(color):
            newChannel = channel + tint[i]
            if newChannel > 255:
                newChannel = 255
            newColor[i] = newChannel
        return tuple(newColor)
        

    
    def __call__(self, entities, gamemap, console, recompute_fov = False):
        player = self.selectPlayer(entities)
        playerPosition = player.getComponent('position')

        tiles = gamemap.calculateTiles()
        entities = entities + tiles
        entities = self.selectRenderable(entities)
        entities = sorted(entities, key=self.getLayer)
        for entity in entities:
            appearance = entity.getComponent('appearance')
            position = entity.getComponent('position')
            physical = entity.getComponent('physical')

            if physical.visible or physical.explored:
                bgcolor = appearance.bgcolor
                fgcolor = appearance.fgcolor
                if appearance.bgcolor != None:
                    if appearance.tint:
                        bgcolor = self.tintColor(bgcolor, appearance.tint)
                    bgcolor = self.multiplyColor(bgcolor, appearance.lighting)
                if appearance.fgcolor != None:
                    fgcolor = self.multiplyColor(fgcolor, appearance.lighting)
                
                console.draw_char(
                    position.x, 
                    position.y, 
                    appearance.character, 
                    bg=bgcolor, 
                    fg=fgcolor
                )
            
        tdl.flush()

        for entity in entities:
            position = entity.getComponent('position')
            console.draw_char(position.x, position.y, ' ', bg=None, fg=None)




