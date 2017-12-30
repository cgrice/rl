import tdl

class RenderSystem(object):
    
    def selectPlayer(self, engine):
        return engine.entityManager.getEntitiesWithComponents('position', 'player')[0]

    def getLayer(self, entity):
        appearance = entity.getComponent('appearance')
        return appearance.layer

    def setColors(self, terminal, fg = None, bg = None):
        if fg == None:
            terminal.color(terminal.color_from_argb(0, 0, 0, 0))
        else:
            terminal.color(terminal.color_from_argb(*fg))
        if bg == None:
            terminal.bkcolor(terminal.color_from_argb(0, 0, 0, 0))
        else:
            terminal.bkcolor(terminal.color_from_argb(*bg))

    def lightTile(self, color, strength, tint = False):
        newColor = [strength, color[1], color[2], color[3]]
        # for i, channel in enumerate(color):
        #     if i == 0:
        #         newChannel = channel *
        #     else:
        #         if tint != False:
        #             channel = channel + tint[i] * ratio
        #         newChannel = int((channel * ratio) // 1)
        #         if newChannel > 255:
        #             newChannel = 255
        #     newColor[i] = newChannel
        return tuple(newColor)

    def __call__(self, engine, previous = None):
        recompute_fov = previous == True
        em = engine.entityManager
        terminal = engine.terminal

        gamemap = engine.getStage()
        entities = em.getEntitiesWithComponents('position', 'appearance', 'physical')
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

                if physical.explored and not physical.visible:
                    bgcolor = (255, 0, 0, 0)
                    fgcolor = (50, 255, 255, 255)
                
                self.setColors(terminal, fg=fgcolor, bg=bgcolor)
                terminal.layer(appearance.layer)

                terminal.put(position.x, position.y, appearance.character)
            
        self.setColors(terminal, fg=(0, 0, 0, 0), bg=(0, 0, 0, 0))


