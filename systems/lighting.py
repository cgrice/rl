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
        minStrength = 1
        maxStrength = strength
        strengthRange = maxStrength - minStrength
        ratio = distance / radius
        return maxStrength - strengthRange * ratio

    def __call__(self, entities, gamemap):
        
        all_visible = set()

        light_sources = [entity for entity in entities if entity.hasComponents('light_source', 'position')]
        
        for source in light_sources:
            light = source.getComponent('light_source')
            visible_tiles = self.calculateVisible(source, gamemap)
            all_visible = all_visible.union(visible_tiles)

            for entity in entities:
                if entity.hasComponents('position', 'physical', 'appearance'):
                    position = entity.getComponent('position')
                    physical = entity.getComponent('physical')
                    appearance = entity.getComponent('appearance')
                    x, y = position.x, position.y
                    visible = (x, y) in visible_tiles
                    physical.visible = visible
                    appearance.lighting = 1

                    if visible:
                        appearance.lighting = light.strength

                    entity.addComponent('appearance', appearance) 
                    entity.addComponent('physical', physical)

            for y in range(gamemap.height):
                for x in range(gamemap.width):
                    visible = (x, y) in visible_tiles
                
                    physical = gamemap.tiles[x][y].getComponent('physical')
                    appearance = gamemap.tiles[x][y].getComponent('appearance')
                    appearance.lighting = 1
                    appearance.tint = False
                    physical.visible = visible

                    if visible:
                        source_position = source.getComponent('position')
                        distance = self._distance(source_position.x, source_position.y, x, y)
                        appearance.lighting = self.calculateStrength(light.radius, distance, light.strength)
                        appearance.tint = light.tint
                        physical.explored = True

                    gamemap.tiles[x][y].addComponent('physical', physical)
                    gamemap.tiles[x][y].addComponent('appearance', appearance)

        return True