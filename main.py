import tdl

from explorer.generators.dungeon import DungeonGenerator
from explorer.systems import RenderSystem, MovementSystem, LightingSystem, TriggerSystem
from explorer.engine import Engine
from explorer.interface import Interface

SCREEN_WIDTH = 81
SCREEN_HEIGHT = 61
MAP_HEIGHT = 51
LIMIT_FPS = 20

# tdl.set_font('dundalk12x12_gs_tc.png', greyscale=True, altLayout=True)
tdl.set_font('dejavu12x12_gs_tc.png', greyscale=True, altLayout=True)

console = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Roguelike", fullscreen=False)

gui = Interface(console,
    width = SCREEN_WIDTH, 
    height = SCREEN_HEIGHT - MAP_HEIGHT, 
    starty = MAP_HEIGHT
)

engine = Engine(console)
engine.addMessage("Welcome to EXPLORER! Get to the bottom of the map to win the game. Happy hunting!", (255,255,255))
engine.gui = gui
engine.addSystems(
    MovementSystem(),
    TriggerSystem(),
    LightingSystem(),
    RenderSystem(),
)
dungeonGenerator = DungeonGenerator(engine)
engine.addStages(
    dungeonGenerator.generate(
        width = SCREEN_WIDTH, height = MAP_HEIGHT, stage = 0,
        density = 1000, twistiness = 70, connectivity = 30, 
        minRoomSize = 2, maxRoomSize = 5,
        exits = 1, entrances = 0
    ),
    dungeonGenerator.generate(
        width = SCREEN_WIDTH, height = MAP_HEIGHT, stage = 1,
        density = 10000, twistiness = 80, connectivity = 8, 
        minRoomSize = 2, maxRoomSize = 5, 
        exits = 1, entrances = 0
    ),
    dungeonGenerator.generate(
        width = SCREEN_WIDTH, height = MAP_HEIGHT, stage = 2,
        density = 100, twistiness = 20, connectivity = 20, 
        minRoomSize = 2, maxRoomSize = 10,
        exits = 1, entrances = 1
    ),
    dungeonGenerator.generate(
        width = SCREEN_WIDTH, height = MAP_HEIGHT, stage = 3,
        density = 100, twistiness = 20, connectivity = 20, 
        minRoomSize = 2, maxRoomSize = 10,
        exits = 1, entrances = 1
    )
)
engine.setStage(0)
engine.addPlayer('Emily', '@', (255,255,255))
engine.profile = False

engine.gui.render(engine)
while engine.run():
    pass
