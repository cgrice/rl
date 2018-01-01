import tdl
import datetime

from explorer.managers import EntityManager
from ecs import Entity
from ecs.components import Position, Player, Physical, Appearance, LightSource, Inventory

class Engine(object):
    '''A game engine.
    '''

    def __init__(self, terminal):
        self.terminal = terminal
        self.systems = []
        self.stages = {}
        self.messages = []
        self.entityManager = EntityManager()
        self.stageIndex = -1
        self.keys = None
        self.gui = None
        self.profile = False
        self.paused = False
        self.won = False

    def run(self):
        # Each system returns an object which is passed along to
        # the next system in the chain. This lets, for example, the
        # movement system tell the lighting system that it needs
        # to recalculate FOV
        prev = None
        for system in self.systems:
            if self.profile:
                start = datetime.datetime.now()
            
            prev = system(self, previous = prev)

            if self.profile:
                end = datetime.datetime.now()
                diff = end - start
                print("%s time: %s" % (system.__class__, diff.microseconds))

        if self.won:
            return False
        
        if self.gui:
            self.gui.render()

        self.terminal.refresh()
        self.terminal.clear()
        
        # Set the input on the engine so that systems can use it
        self.keys = self.getInput()
        exit_game = not self.keys

        if exit_game:
            return False

        if self.keys == 53:
            self.getStage().noFOW = not self.getStage().noFOW

        if self.keys == self.terminal.TK_I:
            self.paused = not self.paused
            self.gui.showInventory = self.paused

        return True

    def addMessage(self, content, color):
        self.messages.append((content, color))

    def addPlayer(self, name, character, color):
        startx, starty = self.getStage().start
        player = Entity()
        player.addComponent('position', Position(x=startx, y=starty, stage=0))
        player.addComponent('appearance', Appearance(
            name, bgcolor=(0,0,0,0), fgcolor=(255, 255, 255, 255), 
            character=0xED0E, layer=10
        ))
        player.addComponent('physical', Physical(visible=True, blocked = True))
        player.addComponent('player', Player())
        player.addComponent('controllable', {})
        player.addComponent('moveable', {})
        player.addComponent('light_source', LightSource(radius=8, tint=(0, 0, 0, 0), strength=255))
        player.addComponent('inventory', Inventory())
        self.entityManager.addEntity(player)


    def addSystems(self, *args):
        for system in args:
            self.systems.append(system)

    def addStages(self, *args):
        index = self.stageIndex
        for stage in args:
            index += 1
            self.stages[index] = stage

    def getInput(self):
        user_input = self.terminal.read()

        exit_keys = [self.terminal.TK_CLOSE, self.terminal.TK_ESCAPE]
        if user_input in exit_keys:
            return False

        # if user_input == self.terminal.TK_ENTER and \
        #    self.terminal.check(self.terminal.TK_ALT):
        #     # Alt+Enter: toggle fullscreen
        #     self.terminal.set('window: fullscreen=true;')

        return user_input

    def addStage(self, index, gamemap):
        gamemap.stageIndex = index
        self.stages[index] = gamemap

    def hasStage(self, index):
        return index in self.stages

    def setStage(self, index):
        if self.stageIndex in self.stages:
            for entity in self.stages[self.stageIndex].getEntities():
                self.entityManager.removeEntity(entity)
        self.stageIndex = index
        for entity in self.stages[index].getEntities():
            self.entityManager.addEntity(entity)
        
    def getStage(self):
        return self.stages[self.stageIndex]