class TriggerSystem(object):

    def __call__(self, engine, previous = None):
        em = engine.entityManager
        try:
            player = em.getEntitiesWithComponents('player')[0]
            entities = em.getEntitiesWithComponents('trigger')
            for entity in entities:
                trigger = entity.getComponent('trigger')
                trigger.run(entity, player)
        except Exception as e:
            raise e
            pass

        return True
