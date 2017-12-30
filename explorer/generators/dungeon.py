from random import choice

from explorer.gamemap import GameMap, Dungeon
from explorer.gamemap.themes.dungeon import STANDARD_DUNGEON
from ecs import Entity
from ecs.components import Position, Appearance, Physical, Trigger, LightSource
from ecs.actions.triggers import MoveStage, LogMessage, AddToInventory
from ecs.conditions.location import SteppedOn
from ecs.conditions.components import HasComponents


DUNGEON_THEMES = [
    ((255, 48, 43, 26), (255, 100, 100, 100)),
    ((255, 22, 0, 30), (255, 85, 53, 85)),
    ((255, 5, 25, 5), (255, 50, 30, 10)),
    ((255, 10, 10, 10), (255, 50, 50, 50)),
    ((255, 40, 40, 60), (255, 100, 100, 140)),
]

GEM_COLORS = {
    'red': (255, 255, 0, 0),
    'green': (255, 0, 255, 0),
    'blue': (255, 0, 0, 255),
}

class DungeonGenerator(object):
    '''A generator which creates a standard RPG dungeon

    A dungeon has rooms and corridors, and is filled with 
    monsters. It has stairs that go up and down to higher 
    and lower levels.
    '''
    def __init__(self, engine):
        self.engine = engine
        self.stage = -1

    def generate(self, 
        width = 81,
        height = 41,
        stage = -1,
        density = 100, 
        twistiness = 10, 
        connectivity = 5, 
        minRoomSize = 2, 
        maxRoomSize = 5,
        exits = 1,
        entrances = 1,
        theme = None
    ):
        self.stage = stage

        if theme != None:
            self.theme = theme
        else:
            self.theme = STANDARD_DUNGEON

        # Create a new map with the specific width, and a dungeon to fill it.
        # We can then generate some entities for walls and floors based on
        # the configuration of the dungeon
        gamemap = GameMap(
            width = width, 
            height = height, 
            stageIndex = stage, 
            theme = self.theme
        )

        dungeon = Dungeon(gamemap, 
            density = density, 
            twistiness = twistiness, 
            connectivity = connectivity, 
            minRoomSize = minRoomSize, 
            maxRoomSize = maxRoomSize
        )
        dungeon.generate()

        # Set up start and exit positions for this dungeon - should be in 
        # the centre of one of the generated rooms.
        startx, starty = dungeon.randomPosition()
        gamemap.start = (startx, starty)
        exitx, exity = dungeon.randomPosition()
        gamemap.exit = (exitx, exity)

        # Set up our exits and entrances! Currently only supports one of each
        # per floor, want to add more later so we can have more confusing dungeons!
        # @TODO: Add multiple exits/entrances
        self._addTransports(gamemap, dungeon, exits = exits, entrances = entrances)

        self._populate(gamemap, dungeon)

        return gamemap

    def _populate(self, gamemap, dungeon):
        gem = Entity()
        gemx, gemy = dungeon.randomPosition()
        gemColor = choice(list(GEM_COLORS.keys()))
        gem.addComponent('position', Position(x=gemx, y=gemy, stage=self.stage))
        gem.addComponent('physical', Physical(blocks_sight = False, blocked = False))
        gem.addComponent('appearance', Appearance('A shiny %s gem' % gemColor, layer=1, character='*', fgcolor=GEM_COLORS[gemColor]))
        # gem.addComponent('light_source', LightSource(radius=2, strength=3, tint=(10,0,0)))
        gemTrigger = Trigger(
            actions = [
                LogMessage(self.engine, message = 'picked up a shiny %s gem' % gemColor),
                AddToInventory(self.engine),
            ],
            conditions = [
                HasComponents('player'),
                SteppedOn(),
            ]
        )
        gem.addComponent('trigger', gemTrigger)
        gem.addComponent('essential', {})
        self.engine.entityManager.addEntity(gem)
        return True

    def _addTransports(self, gamemap, dungeon, exits = 0, entrances = 0):
        for x in range(exits):
            exitx, exity = gamemap.exit
            stairsdown = Entity()
            stairsdown.addComponent('position', Position(x=exitx, y=exity, stage=self.stage))
            stairsdown.addComponent('appearance', Appearance('stairs', 
                layer=1, character=self.theme['tiles']['stairs-down'], 
                fgcolor=(255, 255, 255, 255), 
                bgcolor=(255, 0, 0, 0)))
            stairsdown.addComponent('physical', Physical(blocks_sight = False, blocked = False))
            stairsTrigger = Trigger(
                actions = [
                    MoveStage(self.engine, direction = 1)
                ],
                conditions = [
                    HasComponents('player'),
                    SteppedOn(),
                ]
            )
            stairsdown.addComponent('trigger', stairsTrigger)
            self.engine.entityManager.addEntity(stairsdown)
        for x in range(entrances):
            startx, starty = gamemap.start
            stairsup = Entity()
            stairsup.addComponent('position', Position(x=startx, y=starty, stage=self.stage))
            stairsup.addComponent('appearance', Appearance('stairs', 
                layer=1, character=self.theme['tiles']['stairs-up'], 
                fgcolor=(255, 255, 255, 255)
            ))
            stairsup.addComponent('physical', Physical(blocks_sight = False, blocked = False))
            stairsTrigger = Trigger(
                actions = [MoveStage(self.engine, direction = -1)],
                conditions = [HasComponents('player'),SteppedOn()]
            ) 
            stairsup.addComponent('trigger', stairsTrigger)
            self.engine.entityManager.addEntity(stairsup)
            # gamemap[startx][starty] = stairsup
        