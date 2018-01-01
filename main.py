import tdl
from bearlibterminal import terminal
import time

from explorer.generators.dungeon import DungeonGenerator
from explorer.gamemap.themes.dungeon import GRASS_DUNGEON
from explorer.systems import RenderSystem, ProgressSystem, FOVSystem, \
                             MovementSystem, LightingSystem, TriggerSystem
from ecs.conditions.inventory import HasItems
from explorer.engine import Engine
from explorer.interface import Interface

TITLE = 'Explorer'
SCREEN_WIDTH = 81
SCREEN_HEIGHT = 51
MAP_HEIGHT = 41
LIMIT_FPS = 20

# tdl.set_font('dundalk12x12_gs_tc.png', greyscale=True, altLayout=True)
tdl.set_font('dejavu16x16_gs_tc.png', greyscale=True, altLayout=True)

terminal.open()
terminal.set("font: dejavu16x16_gs_tc.png, size=16x16, codepage=tcod;")
terminal.set("0xE000: tiles16x16.png, size=16x16;")
terminal.set("0xEC00: characters16x16.png, size=16x16;")
terminal.set("0xEFFF: light.png, size=16x16;")
terminal.set("window: title=%s, size=%sx%s, cellsize=16x16;" % (TITLE, SCREEN_WIDTH, SCREEN_HEIGHT))

terminal.printf(SCREEN_WIDTH//2-5, SCREEN_HEIGHT//2-2, 'EXPLORER!')
terminal.printf(SCREEN_WIDTH//2-8, SCREEN_HEIGHT//2, 'Loading maps...')
terminal.refresh()

# y = 0
# x = 0
# for c in range(0xE000, 0xEF00):
#     if y > 51:
#         y = 0
#         x += 1
#     terminal.put(y, x, c)
#     y += 1

# c = 0xE000
# while True:
    
#     terminal.put(0, 0, c)
#     terminal.printf(0, 30, str(hex(c)))
#     terminal.refresh()
#     i = terminal.read()
#     if i == terminal.TK_DOWN:
#         c += 57
#     if i == terminal.TK_UP:
#         c -= 57
#     if i == terminal.TK_RIGHT:
#         c += 1
#     if i == terminal.TK_LEFT:
#         c -= 1
#     if i == terminal.TK_ESCAPE:
#         break
#     pass

engine = Engine(terminal)
engine.addMessage("Welcome to EXPLORER! Get to the bottom of the map to win the game. Happy hunting!", (255,100,100,0))

gui = Interface(engine,
    width = SCREEN_WIDTH, 
    height = SCREEN_HEIGHT, 
    starty = MAP_HEIGHT
)
engine.gui = gui
engine.addSystems(
    MovementSystem(),
    TriggerSystem(),
    FOVSystem(),
    LightingSystem(),
    RenderSystem(),
)
dungeonGenerator = DungeonGenerator(engine)
engine.addStages(
    dungeonGenerator.generate(
        width = SCREEN_WIDTH, height = MAP_HEIGHT, stage = 0,
        density = 1000, twistiness = 70, connectivity = 30, 
        minRoomSize = 2, maxRoomSize = 5,
        exits = 1, entrances = 0, theme = GRASS_DUNGEON,
    ),
    dungeonGenerator.generate(
        width = SCREEN_WIDTH, height = MAP_HEIGHT, stage = 1,
        density = 10000, twistiness = 80, connectivity = 8, 
        minRoomSize = 2, maxRoomSize = 5, 
        exits = 1, entrances = 1
    ),
    dungeonGenerator.generate(
        width = SCREEN_WIDTH, height = MAP_HEIGHT, stage = 2,
        density = 100, twistiness = 20, connectivity = 20, 
        minRoomSize = 2, maxRoomSize = 5,
        exits = 1, entrances = 1
    ),
    dungeonGenerator.generate(
        width = SCREEN_WIDTH, height = MAP_HEIGHT, stage = 3,
        density = 100, twistiness = 20, connectivity = 20, 
        minRoomSize = 2, maxRoomSize = 5,
        exits = 0, entrances = 1
    )
)
gems = engine.entityManager.getEntitiesWithComponents('essential')
essential = [gem.uid for gem in gems]
engine.addSystems(
    ProgressSystem(conditions = [
        HasItems(items = essential)
    ])
)
engine.setStage(0)
engine.addPlayer('Emily', '@', (255,255,255,255))
engine.profile = False

terminal.clear()
engine.gui.render()
while engine.run():
    pass

if engine.won:
    terminal.clear()
    terminal.color(terminal.color_from_argb(255, 255, 255, 255))
    terminal.printf(SCREEN_WIDTH//2-5, SCREEN_HEIGHT//2-2, 'YOU WIN!')
    terminal.refresh()
    terminal.read()