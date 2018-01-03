import tdl
import textwrap

PANEL_HEIGHT = 20
MSG_WIDTH = 38
STATS_WIDTH = 40
BORDER_SIZE = 1
INVENTORY_WIDTH = 35
INVENTORY_HEIGHT = 30

class Interface(object):

    def __init__(self, engine, width = 0, height = 0, starty = 0):
        self.engine = engine
        self.terminal = engine.terminal
        self.starty = starty
        self.startx = 0
        self.width = width
        self.height = height
        self.messages = []
        self.showInventory = False

    def _clear(self):
        self.terminal.layer(100)
        self.terminal.bkcolor(self.terminal.color_from_argb(255, 255, 255, 200))
        self.terminal.color(self.terminal.color_from_argb(255, 255, 255, 255))
        # self.terminal.clear_area(self.startx, self.starty, self.width, self.height)

    def _rect(self, x, y, w, h, color):
        self.terminal.bkcolor(self.terminal.color_from_argb(*color))
        self.terminal.clear_area(x, y, w, h)

    def _widget(self, x, y, w, h, title = False):
        # topLeft = 0xE5BD
        # topRight = 0xE5BF
        # bottomLeft = 0xE62F
        # bottomRight = 0xE631
        # topBorder = 0xE5BE
        # leftBorder = 0xE5F6
        # rightBorder = 0xE5F8
        # bottomBorder = 0xE630
        # background = 0xE5F7
        topLeft = 0xE5BA
        topRight = 0xE5BC
        bottomLeft = 0xE62C
        bottomRight = 0xE62E
        topBorder = 0xE5BB
        leftBorder = 0xE5F3
        rightBorder = 0xE5F5
        bottomBorder = 0xE62D
        background = 0xE5F4

        self.terminal.put(x, y, topLeft)
        self.terminal.put(x+w, y, topRight)
        self.terminal.put(x+w, y+h, bottomRight)
        self.terminal.put(x, y+h, bottomLeft)
        for xPos in range(x+1, x+w):
            self.terminal.put(xPos, y, topBorder)
            self.terminal.put(xPos, y+h, bottomBorder)
            for yPos in range(y+1, y+h):
                self.terminal.put(x, yPos, leftBorder)
                self.terminal.put(x+w, yPos, rightBorder)
                self.terminal.put(xPos, yPos, background)

        if title != False:
            centerx = x + (w // 2) - (len(title) // 2)
            self.terminal.layer(111)
            self.terminal.bkcolor(self.terminal.color_from_argb(255, 0, 0, 0))
            self.terminal.color(self.terminal.color_from_argb(255, 0, 0, 0))
            self.terminal.print(centerx, y+2, title)

    def render(self):
        self._clear()
        self._widget(1, self.starty, MSG_WIDTH, self.height)
        self._widget(MSG_WIDTH+3, self.starty, MSG_WIDTH, self.height)
        self.renderStats()
        self.renderMessages(self.engine.messages)
        if self.showInventory:
            self.renderInventory()

        self.terminal.layer(0)
        self.terminal.color(self.terminal.color_from_argb(255, 0, 0, 0))
        self.terminal.bkcolor(self.terminal.color_from_argb(255, 0, 0, 0))

    def renderInventory(self):
        startx = (self.width // 2) - (INVENTORY_WIDTH // 2)
        starty = (self.height // 4) - (INVENTORY_HEIGHT // 4)
        self.terminal.layer(110)
        self.terminal.color(self.terminal.color_from_argb(255, 255, 255, 255))
        self.terminal.bkcolor(self.terminal.color_from_argb(255, 255, 255, 255))
        self._widget(startx, starty, INVENTORY_WIDTH, INVENTORY_HEIGHT, title="CHARACTER INVENTORY")

        em = self.engine.entityManager
        player = em.getEntitiesWithComponents('player', 'appearance', 'position', 'inventory')[0]
        inventory = player.getComponent('inventory')
        self.terminal.layer(111)
        index = 5
        for itemid in inventory.items:
            item = em.getEntity(itemid)
            appearance = item.getComponent('appearance')
            self.terminal.print(startx+1, starty+index, appearance.name)
            index += 1


    def renderStats(self):
        em = self.engine.entityManager
        statsX = MSG_WIDTH+BORDER_SIZE+3
        statsY = self.starty+BORDER_SIZE
        
        player = em.getEntitiesWithComponents('player', 'appearance', 'position', 'inventory')[0]
        appearance = player.getComponent('appearance')
        position = player.getComponent('position')
        inventory = player.getComponent('inventory')
        name = "Player: %s" % appearance.name
        health = "HP:     50 / 50"
        position = "Coords: %s,%s" % (position.x, position.y)
        floor = "Floor:  %s" % self.engine.stageIndex
        inventory = "%s items in bag" % (len(inventory.items))

        self.terminal.layer(101)
        self.terminal.color(self.terminal.color_from_argb(255, 0, 0, 0))
        self.terminal.print(statsX, statsY, name)
        self.terminal.print(statsX, statsY + 1, health)
        self.terminal.print(statsX, statsY + 3, position)
        self.terminal.print(statsX, statsY + 4, floor)
        self.terminal.print(statsX, statsY + 5, inventory)

    def renderMessages(self, messages):
        self.terminal.layer(101)
        self.terminal.bkcolor(self.terminal.color_from_argb(255, 255, 255, 255))
        self.terminal.color(self.terminal.color_from_argb(255, 0, 0, 0))

        messages = self.bufferMessages(messages[-8:])
        
        y = self.starty + BORDER_SIZE
        for message in messages:
            content, color = message
            self.terminal.color(self.terminal.color_from_argb(255, 0, 0, 0))
            # self.terminal.color(self.terminal.color_from_argb(*color))
            self.terminal.print(2, y, content)
            y += 1

    def bufferMessages(self, messages):
        bufferedMessages = []
        for message in reversed(messages):
            content, color = message
            #split the message if necessary, among multiple lines
            lines = textwrap.wrap(content, MSG_WIDTH-1)
 
            for line in lines:
                #if the buffer is full, remove the first line to make room for the new one
                if len(bufferedMessages) == self.height - 2:
                    del bufferedMessages[-1]
        
                #add the new line as a tuple, with the text and the color
                bufferedMessages.append((line, color))
        return bufferedMessages
    # def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color):
    #     #render a bar (HP, experience, etc). first calculate the width of the bar
    #     bar_width = int(float(value) / maximum * total_width)
    
    #     #render the background first
    #     panel.draw_rect(x, y, total_width, 1, None, bg=back_color)
    
    #     #now render the bar on top
    #     if bar_width > 0:
    #         panel.draw_rect(x, y, bar_width, 1, None, bg=bar_color)
    
    #     #finally, some centered text with the values
    #     text = name + ': ' + str(value) + '/' + str(maximum)
    #     x_centered = x + (total_width-len(text))//2
    #     panel.draw_str(x_centered, y, text, fg=colors.white, bg=None)