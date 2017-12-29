import tdl
import time

from explorer.generators.dungeon import DungeonGenerator
from explorer.systems import RenderSystem, ProgressSystem, \
                             MovementSystem, LightingSystem, TriggerSystem
from ecs.conditions.inventory import HasItems
from explorer.engine import Engine
from explorer.interface import Interface

SCREEN_WIDTH = 81
SCREEN_HEIGHT = 51
MAP_HEIGHT = 41
LIMIT_FPS = 20

# tdl.set_font('dundalk12x12_gs_tc.png', greyscale=True, altLayout=True)
tdl.set_font('dejavu16x16_gs_tc.png', greyscale=True, altLayout=True)

console = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Roguelike", fullscreen=False)
console.draw_str(SCREEN_WIDTH//2-5, SCREEN_HEIGHT//2-2, 'EXPLORER!', bg=(0,0,0))
console.draw_str(SCREEN_WIDTH//2-8, SCREEN_HEIGHT//2, 'Loading maps...', bg=(0,0,0))
tdl.flush()

engine = Engine(console)
engine.addMessage("Welcome to EXPLORER! Get to the bottom of the map to win the game. Happy hunting!", (255,255,255))

gui = Interface(engine, console,
    width = SCREEN_WIDTH, 
    height = SCREEN_HEIGHT, 
    starty = MAP_HEIGHT
)
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
        exits = 0, entrances = 0,
        theme = 0
    ),
    # dungeonGenerator.generate(
    #     width = SCREEN_WIDTH, height = MAP_HEIGHT, stage = 1,
    #     density = 10000, twistiness = 80, connectivity = 8, 
    #     minRoomSize = 2, maxRoomSize = 5, 
    #     exits = 1, entrances = 1
    # ),
    # dungeonGenerator.generate(
    #     width = SCREEN_WIDTH, height = MAP_HEIGHT, stage = 2,
    #     density = 100, twistiness = 20, connectivity = 20, 
    #     minRoomSize = 2, maxRoomSize = 5,
    #     exits = 1, entrances = 1
    # ),
    # dungeonGenerator.generate(
    #     width = SCREEN_WIDTH, height = MAP_HEIGHT, stage = 3,
    #     density = 100, twistiness = 20, connectivity = 20, 
    #     minRoomSize = 2, maxRoomSize = 5,
    #     exits = 0, entrances = 1
    # )
)
gems = engine.entityManager.getEntitiesWithComponents('essential')
essential = [gem.uid for gem in gems]
engine.addSystems(
    ProgressSystem(conditions = [
        HasItems(items = essential)
    ])
)
engine.setStage(0)
engine.addPlayer('Emily', '@', (255,255,255))
engine.profile = True

console.clear()
engine.gui.render()
while engine.run():
    pass

if engine.won:
    console.draw_str(SCREEN_WIDTH//2-5, SCREEN_HEIGHT//2-2, 'YOU WIN!', bg=(0,0,0))
    tdl.flush()
    tdl.event.key_wait()