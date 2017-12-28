class SteppedOn(object):

    def __call__(self, source, target):
        if target.hasComponents('position'):
            if source.hasComponents('position'):
                target_position = target.getComponent('position')
                source_position = source.getComponent('position')
                if source_position.x == target_position.x and \
                   source_position.y == target_position.y:
                   return True
        return False