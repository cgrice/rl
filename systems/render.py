import tdl

class RenderSystem(object):
    
    def selectPlayer(self, engine):
        return engine.getEntitiesWithComponents('position', 'player')[0]

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
        

    
    def __call__(self, engine, gamemap, console, recompute_fov = False):
        player = self.selectPlayer(engine)
        playerPosition = player.getComponent('position')

        tiles = gamemap.calculateTiles()
        entities = engine.getEntitiesWithComponents('position', 'appearance', 'physical')
        entities = entities + tiles
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




