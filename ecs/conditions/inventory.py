class HasItems(object):

    def __init__(self, items = []):
        self.items = items

    def __call__(self, source, target):
        inventory = target.getComponent('inventory')
        for item in self.items:
            if item not in inventory.items:
                return False
        return True
