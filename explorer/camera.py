class Camera(object):

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def move(self, targetX, targetY, stage):
        x = int(targetX - (self.width // 2))
        y = int(targetY - (self.height // 2))

        if x < 0:
            x = 0

        if y < 0:
            y = 0

        if x > stage.width - self.width:
            x = stage.width - self.width

        if y > stage.height - self.height:
            y = stage.height - self.height

        self.x = x
        self.y = y

    def toCameraPosition(self, x, y):
        
        x = x - self.x
        y = y - self.y

        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return -1, -1

        return x, y