class Trigger(object):

    def __init__(self, condition = None, action = None):
        self.condition = condition
        self.action = action

    def run(self, source, target, **kwargs):
        if self.action != None:
            if self.condition != None:
                if self.condition(source, target):
                    self.action(source, target, **kwargs)
            else:
                self.action(source, target, **kwargs)