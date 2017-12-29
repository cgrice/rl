import tdl
import datetime

from explorer.managers import EntityManager
from ecs import Entity
from ecs.components import Position, Player, Physical, Appearance, LightSource

class Engine(object):
    '''A game engine.
    '''

    def __init__(self, console):
        self.console = console
        self.systems = []
        self.stages = []
        self.messages = []
        self.entityManager = EntityManager()
        self.stageIndex = -1
        self.keys = None
        self.gui = None
        self.profile = False

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

        if self.gui:
            self.gui.render(self)

        tdl.flush()
        self.console.clear()
        
        # Set the input on the engine so that systems can use it
        self.keys = self.getInput()
        exit_game = not self.keys

        if exit_game or tdl.event.is_window_closed():
            return False

        if self.keys.key == 'TEXT' and self.keys.text == '§':
            self.getStage().noFOW = not self.getStage().noFOW

        

        return True

    def addMessage(self, content, color):
        self.messages.append((content, color))

    def addPlayer(self, name, character, color):
        startx, starty = self.getStage().start
        player = Entity()
        player.addComponent('position', Position(x=startx, y=starty, stage=0))
        player.addComponent('appearance', Appearance(name, fgcolor=(255,255,255), character='@', layer=1))
        player.addComponent('physical', Physical(visible=True, blocked = True))
        player.addComponent('player', Player())
        player.addComponent('controllable', {})
        player.addComponent('moveable', {})
        player.addComponent('light_source', LightSource(radius=8, tint=(20, 20, 5), strength=2.5))
        self.entityManager.addEntity(player)


    def addSystems(self, *args):
        for system in args:
            self.systems.append(system)

    def addStages(self, *args):
        for stage in args:
            self.stages.append(stage)

    def getInput(self):
        user_input = tdl.event.key_wait()

        if user_input.key == 'ENTER' and user_input.alt:
            #Alt+Enter: toggle fullscreen
            tdl.set_fullscreen(not tdl.get_fullscreen())
        elif user_input.key == 'ESCAPE':
            return False  #exit game

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