class Entity:

    def __init__(self, x, y, character, color):
        self.x = x
        self.y = y
        self.character = character
        self.color = color

    def draw(self, console):
        console.draw_char(self.x, self.y, self.character, bg=None, fg=self.color)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def clear(self, console):
        console.draw_char(self.x, self.y, ' ', bg=None, fg=None)



