class MovementSystem(object):

    def selectControllable(self, entities):
        return [
            entity for entity in entities 
            if entity.hasComponents('moveable', 'controllable', 'position')
        ]


    def __call__(self, keys, entities, gamemap, console):
        fov_recompute = False
        toMove = self.selectControllable(entities)
        
        for entity in toMove:
            dx, dy = (0, 0)
            position = entity.getComponent('position')

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