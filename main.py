import tdl

from explorer.generators.dungeon import DungeonGenerator
from explorer.systems import RenderSystem, MovementSystem, LightingSystem, TriggerSystem
from explorer.engine import Engine

SCREEN_WIDTH = 81
SCREEN_HEIGHT = 76
MAP_HEIGHT = 51
LIMIT_FPS = 20

tdl.set_font('dundalk12x12_gs_tc.png', greyscale=True, altLayout=True)
console = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Roguelike", fullscreen=False)

engine = Engine(console)
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
        density = 10000, twistiness = 80, connectivity = 8, 
        minRoomSize = 2, maxRoomSize = 5, 
        exits = 1, entrances = 0
    ),
    dungeonGenerator.generate(
        width = SCREEN_WIDTH, height = MAP_HEIGHT, stage = 1,
        density = 100, twistiness = 20, connectivity = 20, 
        minRoomSize = 2, maxRoomSize = 10,
        exits = 1, entrances = 1
    )
)
engine.setStage(0)
engine.addPlayer('@', (255,255,255))
engine.profile = False

while engine.run():
    pass
