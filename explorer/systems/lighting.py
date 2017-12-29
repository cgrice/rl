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

    def __call__(self, engine, previous = None):
        if engine.paused:
            return previous
        
        gamemap = engine.getStage()
        em = engine.entityManager
        
        all_visible = set()

        light_sources = em.getEntitiesWithComponents('light_source', 'position')
        
        for source in light_sources:
            source_position = source.getComponent('position')

            if source_position.stage != gamemap.stageIndex:
                continue
            
            light = source.getComponent('light_source')
            
            visible_tiles = self.calculateVisible(source, gamemap)
            all_visible = all_visible.union(visible_tiles)

            for entity in em.getEntitiesWithComponents(
                'position', 'physical', 'appearance'
            ):
                position = entity.getComponent('position')
                appearance = entity.getComponent('appearance')

                if position.stage != gamemap.stageIndex:
                    continue

                physical = entity.getComponent('physical')
                x, y = position.x, position.y
                visible = (x, y) in visible_tiles

                physical.visible = visible
                appearance.lighting = 1
                appearance.tint = False

                if visible:
                    distance = self._distance(source_position.x, source_position.y, x, y)
                    appearance.lighting = self.calculateStrength(light.radius, distance, light.strength)
                    appearance.tint = light.tint

                if visible or gamemap.noFOW:
                    physical.explored = True

                entity.addComponent('appearance', appearance)
                entity.addComponent('physical', physical)

            # for y in range(gamemap.height):
            #     for x in range(gamemap.width):
            #         visible = (x, y) in visible_tiles
                
            #         physical = gamemap.tiles[x][y].getComponent('physical')
            #         appearance = gamemap.tiles[x][y].getComponent('appearance')
            #         position = gamemap.tiles[x][y].getComponent('position')

            #         if position.stage != gamemap.stageIndex:
            #             continue

            #         appearance.lighting = 1
            #         appearance.tint = False
            #         physical.visible = visible

            #         if visible:
            #             distance = self._distance(source_position.x, source_position.y, x, y)
            #             appearance.lighting = self.calculateStrength(light.radius, distance, light.strength)
            #             appearance.tint = light.tint

            #         if visible or gamemap.noFOW:
            #             physical.explored = True

            #         gamemap.tiles[x][y].addComponent('physical', physical)
            #         gamemap.tiles[x][y].addComponent('appearance', appearance)