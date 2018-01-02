import tdl
import math

FOV_ALGO = 'SHADOW'  #default FOV algorithm
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10

class LightingSystem(object):

    def _distance(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    def calculateVisible(self, source, gamemap):
        position = source.getComponent('position')
        light = source.getComponent('light_source')
        visible_tiles = tdl.map.quickFOV(
            position.x, position.y, gamemap.is_visible,
            fov=FOV_ALGO,
            radius=light.radius,
            lightWalls=FOV_LIGHT_WALLS
        )
        return visible_tiles

    def calculateStrength(self, radius, distance, strength):
        maxStrength = 255
        minStrength = 40
        strengthRange = maxStrength - minStrength
        ratio = distance / radius
        return maxStrength - int(strengthRange * ratio)

    def _tint(self, original, tint):
        new = original + tint
        if new > 255:
            new = 255
        return 255

    def lightTile(self, color, strength):
        newColor = [strength, color[1], color[2], color[3]]
            
        return tuple(newColor)

    def _averageColor(self, colors):
        alpha = 0
        r = 0
        g = 0
        b = 0

        for color in colors:
            alpha += color[0]
            r += color[1]
            g += color[2]
            b += color[3]
        
        alpha = int((alpha / len(colors)) // 1)
        r = int((r / len(colors)) // 1)
        g = int((g / len(colors)) // 1)
        b = int((b / len(colors)) // 1)

        # if alpha > 255:
        #     alpha = 255

        return (alpha, r, g, b)

    def __call__(self, engine, previous = None):
        recalculate_fov = previous

        if engine.paused or recalculate_fov == False:
            return previous

        lightingMap = {}
        
        gamemap = engine.getStage()
        em = engine.entityManager
        camera = engine.camera
        
        light_sources = em.getEntitiesWithComponents('light_source', 'position')
        
        valid_sources = 0
        for source in light_sources:
            source_position = source.getComponent('position')
            if source_position.stage != gamemap.stageIndex:
                continue
            visible_tiles = self.calculateVisible(source, gamemap)
            for (x, y) in visible_tiles:
                mapX, mapY = camera.toCameraPosition(x, y)
                if (mapX, mapY) not in lightingMap:
                    lightingMap[(mapX, mapY)] = set()
                lightingMap[(mapX, mapY)].add(source)
            valid_sources += 1

        if valid_sources == 0:
            return previous


        for y in range(camera.height):
            for x in range(camera.width):
                try:
                    mapX = x + camera.x
                    mapY = y + camera.y
                    entities = gamemap[mapX][mapY]
                except Exception as e:
                    raise e
                    continue

                for entity in entities:
                    position = entity.getComponent('position')
                    appearance = entity.getComponent('appearance')

                    if position.stage != gamemap.stageIndex or appearance.layer != 0:
                        continue

                    lit = (position.x, position.y) in lightingMap

                    if lit:
                        
                        fgcolors = []
                        bgcolors = []

                        for source in lightingMap[(mapX, mapY)]:
                            light = source.getComponent('light_source')
                            source_position = source.getComponent('position')

                            appearance = entity.getComponent('appearance')

                            distance = self._distance(source_position.x, source_position.y, x, y)
                            lighting = self.calculateStrength(light.radius, distance, light.strength)
                            
                            if light.tint:
                                bgcolor = self.lightTile(light.tint, lighting)
                                bgcolors.append(bgcolor)
                            if appearance.fgcolor != None:
                                fgcolor = self.lightTile(appearance.fgcolor, lighting)
                                fgcolors.append(fgcolor)

                            
                        appearance.bgcolor = self._averageColor(bgcolors)
                        appearance.fgcolor = self._averageColor(fgcolors)

                        entity.addComponent('appearance', appearance)
                
        return previous