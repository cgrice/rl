import tdl
import textwrap

PANEL_HEIGHT = 20
MSG_WIDTH = 40
STATS_WIDTH = 40
BORDER_SIZE = 1
INVENTORY_WIDTH = 41
INVENTORY_HEIGHT = 41

class Interface(object):

    def __init__(self, engine, console, width = 0, height = 0, starty = 0):
        self.root = console
        self.starty = starty
        self.width = width
        self.height = height
        self.messages = []
        self.engine = engine
        
        self.panel = tdl.Console(self.width, self.height)
        self.inventory = tdl.Console(INVENTORY_WIDTH, INVENTORY_HEIGHT)
        self.showInventory = False

    def render(self):
        self.panel.clear(bg=(20,20,50))
        self.panel.draw_rect(0, 0, self.width, BORDER_SIZE, 1, bg=(100,100,120))
        self.panel.draw_rect(0, self.height-1, self.width, BORDER_SIZE, 1, bg=(100,100,120))
        self.panel.draw_rect(MSG_WIDTH, 0, BORDER_SIZE, self.height, 1, bg=(100,100,120))
        self.renderStats()
        self.renderMessages(self.engine.messages)
        self.root.blit(self.panel, 0, self.starty, self.width, self.height)
        if self.showInventory:
            self.renderInventory()

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
        startStats = MSG_WIDTH+BORDER_SIZE
        player = em.getEntitiesWithComponents('player', 'appearance', 'position', 'inventory')[0]
        appearance = player.getComponent('appearance')
        position = player.getComponent('position')
        inventory = player.getComponent('inventory')
        name = "Player: %s" % appearance.name
        health = "HP:     50 / 50"
        position = "Coords: %s,%s" % (position.x, position.y)
        floor = "Floor:  %s" % self.engine.stageIndex
        inventory = "%s items in bag" % (len(inventory.items))

        self.panel.draw_str(startStats, BORDER_SIZE, name, bg=None, fg=(255,255,255))
        self.panel.draw_str(startStats, BORDER_SIZE + 1, health, bg=None, fg=(255,255,255))
        self.panel.draw_str(startStats, BORDER_SIZE + 3, position, bg=None, fg=(255,255,255))
        self.panel.draw_str(startStats, BORDER_SIZE + 4, floor, bg=None, fg=(255,255,255))
        self.panel.draw_str(startStats, BORDER_SIZE + 5, inventory, bg=None, fg=(255,255,255))

    def renderMessages(self, messages):
        messages = self.bufferMessages(messages[-8:])
        
        y = 1
        for message in messages:
            content, color = message
            self.panel.draw_str(0, y, content, bg=None, fg=color)
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