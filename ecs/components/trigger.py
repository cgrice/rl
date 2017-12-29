class Trigger(object):

    def __init__(self, conditions = [], actions = []):
        self.conditions = conditions
        self.actions = actions

    def run(self, source, target, **kwargs):
        if len(self.conditions) > 0:
            for condition in self.conditions:
                if condition(source, target) == False:
                    return False
                
        for action in self.actions:
            action(source, target, **kwargs)