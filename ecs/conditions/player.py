class Interacted(object):

    def __call__(self, source, target):
        interactable = source.getComponent('interactable')
        print(interactable)
        if interactable != False and interactable.interacted:
            return True
        return False
