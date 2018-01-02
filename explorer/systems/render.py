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

    def lightTile(self, terminal, x, y, color):
        self.setColors(terminal, fg=color)
        terminal.layer(100)

        terminal.put(x, y, 0xEFFF)

    def __call__(self, engine, previous = None):
        recompute_fov = previous == True

        em = engine.entityManager
        terminal = engine.terminal
        camera = engine.camera
        gamemap = engine.getStage()
        
        # print(camera.height+1, camera.width+1)
        # print(camera.x, camera.y)
        for y in range(camera.height):
            for x in range(camera.width):
                try:
                    mapX = x + camera.x
                    mapY = y + camera.y
                    entities = gamemap[mapX][mapY]
                except Exception as e:
                    raise e
                    # continue

                for entity in entities:
                    position = entity.getComponent('position')

                    physical = entity.getComponent('physical')

                    appearance = entity.getComponent('appearance')

                    if position == False or position.stage != gamemap.stageIndex:
                        continue
                        

                    if physical.visible or physical.explored:
                        appearance = entity.getComponent('appearance')

                        bgcolor = appearance.bgcolor
                        fgcolor = appearance.fgcolor
                        
                        if physical.explored and not physical.visible:
                            bgcolor = (255, 0, 0, 0)
                            fgcolor = (40, 255, 255, 255)


                        self.setColors(terminal, fg=fgcolor, bg=bgcolor)
                        terminal.layer(appearance.layer)

                        x, y = camera.toCameraPosition(position.x, position.y)
                        terminal.put(x, y, appearance.character)

        self.setColors(terminal, fg=(0, 0, 0, 0), bg=(0, 0, 0, 0))


