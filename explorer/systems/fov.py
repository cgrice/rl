import tdl
import math

FOV_ALGO = 'SHADOW'  #default FOV algorithm
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10

class FOVSystem(object):

    def _distance(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    def calculateVisible(self, source, gamemap):
        position = source.getComponent('position')
        visible_tiles = tdl.map.quickFOV(
            position.x, position.y, gamemap.is_visible,
            fov=FOV_ALGO,
            radius=8,
            lightWalls=FOV_LIGHT_WALLS
        )
        return visible_tiles

    def __call__(self, engine, previous = None):
        recompute_fov = previous
        if engine.paused or recompute_fov == False:
            return previous

        lightingMap = {}
        
        gamemap = engine.getStage()
        camera = engine.camera
        em = engine.entityManager
        
        player = em.getEntitiesWithComponents('player', 'position')[0]
        
        visible_tiles = self.calculateVisible(player, gamemap)

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
                    if position == False or position.stage != gamemap.stageIndex:
                        continue

                    physical = entity.getComponent('physical')
                    # x, y = position.x, position.y
                    visible = (position.x, position.y) in visible_tiles

                    physical.visible = visible

                    if visible or gamemap.noFOW:
                        physical.explored = True

                    entity.addComponent('physical', physical)