class TriggerSystem(object):

    def __call__(self, engine, console):
        try:
            player = engine.getEntitiesWithComponents('player')[0]
            entities = engine.getEntitiesWithComponents('trigger')

            for entity in entities:
                trigger = entity.getComponent('trigger')
                trigger.run(entity, player)
        except Exception as e:
            raise e

        
        return False
