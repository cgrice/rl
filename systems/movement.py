class MovementSystem(object):

    def __call__(self, keys, engine, console):
        gamemap = engine.getStage()

        fov_recompute = False
        toMove = engine.getEntitiesWithComponents('position', 'moveable', 'controllable')
        
        for entity in toMove:
            position = entity.getComponent('position')

            if position.stage != gamemap.stageIndex:
                continue
            
            dx, dy = (0, 0)

            if keys.key == 'UP':
                dy -= 1 
                fov_recompute = True
            elif keys.key == 'DOWN':
                dy += 1
                fov_recompute = True
            elif keys.key == 'LEFT':
                dx -= 1
                fov_recompute = True
            elif keys.key == 'RIGHT':
                dx += 1
                fov_recompute = True

            newX = position.x + dx
            newY = position.y + dy

            if gamemap.is_blocked(newX, newY) == False:
                position.x = newX
                position.y = newY
                entity.addComponent('position', position)
            else:
                fov_recompute = False

        return fov_recompute