class Inventory(object):

    def __init__(self, intitial = set()):
        self.items = intitial

    def addItem(self, uid):
        self.items.add(uid)

    def removeItem(self, uid):
        self.items.remove(uid)

