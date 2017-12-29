import tdl

class RenderSystem(object):
    
    def selectPlayer(self, engine):
        return engine.entityManager.getEntitiesWithComponents('position', 'player')[0]

    def getLayer(self, entity):
        appearance = entity.getComponent('appearance')
        return appearance.layer

    def lightTile(self, color, ratio, tint = False):
        newColor = [0, 0, 0]
        for i, channel in enumerate(color):
            if tint != False:
                channel = channel + tint[i] * ratio
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
        
    def __call__(self, engine, previous = None):
        recompute_fov = previous == True
        em = engine.entityManager
        console = engine.console

        gamemap = engine.getStage()
        entities = em.getEntitiesWithComponents('position', 'appearance', 'physical')
        entities = sorted(entities, key=self.getLayer)
        for entity in entities:
            position = entity.getComponent('position')
            if position.stage != gamemap.stageIndex:
                continue

            appearance = entity.getComponent('appearance')
            physical = entity.getComponent('physical')

            if physical.visible or physical.explored:
                bgcolor = appearance.bgcolor
                fgcolor = appearance.fgcolor
                if appearance.bgcolor != None:
                    bgcolor = self.lightTile(bgcolor, appearance.lighting, tint=appearance.tint)
                if appearance.fgcolor != None:
                    fgcolor = self.lightTile(fgcolor, appearance.lighting)
                
                console.draw_char(
                    position.x, 
                    position.y, 
                    appearance.character, 
                    bg=bgcolor, 
                    fg=fgcolor
                )
            
        # for entity in entities:
        #     position = entity.getComponent('position')
        #     console.draw_char(position.x, position.y, ' ', bg=None, fg=None)




