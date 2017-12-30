import tdl
import textwrap

PANEL_HEIGHT = 20
MSG_WIDTH = 40
STATS_WIDTH = 40
BORDER_SIZE = 1
INVENTORY_WIDTH = 41
INVENTORY_HEIGHT = 41

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
        self.terminal.layer(0)
        self.terminal.bkcolor(self.terminal.color_from_argb(255, 20, 20, 50))
        self.terminal.clear_area(self.startx, self.starty, self.width, self.height)

    def _rect(self, x, y, w, h, color):
        self.terminal.bkcolor(self.terminal.color_from_argb(*color))
        self.terminal.clear_area(x, y, w, h)

    def render(self):
        self._clear()
        self._rect(0, self.starty, self.width, BORDER_SIZE, (255,100,100,120))
        self._rect(0, self.height-1, self.width, BORDER_SIZE, (255,100,100,120))
        self._rect(MSG_WIDTH, self.starty, BORDER_SIZE, self.height, (255,100,100,120))
        self.renderStats()
        self.renderMessages(self.engine.messages)
        # self.root.blit(self.panel, 0, self.starty, self.width, self.height)
        # if self.showInventory:
        #     self.renderInventory()

        self.terminal.layer(0)
        self.terminal.color(self.terminal.color_from_argb(0, 0, 0, 0))
        self.terminal.bkcolor(self.terminal.color_from_argb(0, 0, 0, 0))

    def renderInventory(self):
        self.inventory.clear()
        em = self.engine.entityManager
        player = em.getEntitiesWithComponents('player', 'appearance', 'position', 'inventory')[0]
        inventory = player.getComponent('inventory')

        startx = 0
        starty = 0
        centerx = INVENTORY_WIDTH // 2
        self.inventory.draw_rect(0, 0, INVENTORY_WIDTH, INVENTORY_HEIGHT, 1, bg=(50,20,50))
        self.inventory.draw_rect(0, 0, INVENTORY_WIDTH, BORDER_SIZE, 1, bg=(100,100,120))
        self.inventory.draw_rect(INVENTORY_WIDTH - 1, 0, BORDER_SIZE, INVENTORY_HEIGHT, 1, bg=(100,100,120))
        self.inventory.draw_str(centerx - 10, 2, 'CHARACTER INVENTORY', bg=None, fg=(255,255,255))

        index = 4
        for itemid in inventory.items:
            item = em.getEntity(itemid)
            appearance = item.getComponent('appearance')
            self.inventory.draw_str(1, index, appearance.name, fg=(255,255,255), bg=None)

        self.root.blit(self.inventory, startx, starty, INVENTORY_WIDTH, INVENTORY_HEIGHT)


    def renderStats(self):
        em = self.engine.entityManager
        statsX = MSG_WIDTH+BORDER_SIZE
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

        self.terminal.layer(1)
        self.terminal.color(self.terminal.color_from_argb(255, 255, 255, 255))
        self.terminal.print(statsX, statsY, name)
        self.terminal.print(statsX, statsY + 1, health)
        self.terminal.print(statsX, statsY + 3, position)
        self.terminal.print(statsX, statsY + 4, floor)
        self.terminal.print(statsX, statsY + 5, inventory)

    def renderMessages(self, messages):
        messages = self.bufferMessages(messages[-8:])
        
        y = self.starty + BORDER_SIZE
        for message in messages:
            content, color = message
            self.terminal.layer(1)
            self.terminal.color(self.terminal.color_from_argb(*color))
            self.terminal.print(0, y, content)
            y += 1

    def bufferMessages(self, messages):
        bufferedMessages = []
        for message in reversed(messages):
            content, color = message
            #split the message if necessary, among multiple lines
            lines = textwrap.wrap(content, MSG_WIDTH)
 
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