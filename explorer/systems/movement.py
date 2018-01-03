class MovementSystem(object):

    def __call__(self, engine, previous = None):
        if engine.paused:
            return previous

        keys = engine.keys

        if keys == None:
            return previous
        
        em = engine.entityManager
        gamemap = engine.getStage()
        terminal = engine.terminal

        fov_recompute = False
        toMove = em.getEntitiesWithComponents('position', 'moveable', 'controllable')
        
        for entity in toMove:
            position = entity.getComponent('position')

            if position.stage != gamemap.stageIndex:
                continue
            
            dx, dy = (0, 0)

            if keys == terminal.TK_UP:
                dy -= 1 
                fov_recompute = True
            elif keys == terminal.TK_DOWN:
                dy += 1
                fov_recompute = True
            elif keys == terminal.TK_LEFT:
                dx -= 1
                fov_recompute = True
            elif keys == terminal.TK_RIGHT:
                dx += 1
                fov_recompute = True

            newX = position.x + dx
            newY = position.y + dy

            entities = gamemap[newX][newY]

            for mapEntity in entities:

                interactable = mapEntity.getComponent('interactable')
                if interactable != False:
                    interactable.interacted = True
                    mapEntity.addComponent('interactable', interactable)

            if gamemap.is_blocked(newX, newY) == False:
                gamemap[position.x][position.y].remove(entity)
                position.x = newX
                position.y = newY
                entity.addComponent('position', position)
                engine.camera.move(newX, newY, gamemap)
                gamemap[newX][newY].add(entity)
            else:
                fov_recompute = False

        return fov_recompute