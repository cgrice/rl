class HasComponents(object):

    def __init__(self, *args):
        self.components = args

    def __call__(self, source, target):
        return target.hasComponents(*self.components)