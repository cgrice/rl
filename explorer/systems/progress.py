class ProgressSystem(object):

    def __init__(self, conditions = []):
        self.conditions = conditions

    def __call__(self, engine, previous = None):
        em = engine.entityManager
        player = em.getEntitiesWithComponents('player')[0]
        for condition in self.conditions:
            if condition(player, player) == False: 
                return previous
        
        engine.won = True
        