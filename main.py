import tdl
import datetime
from random import randint

from ecs import Entity
from ecs.components import Position, Appearance, Player, \
                           Physical, LightSource, Trigger
from ecs.actions.triggers import MoveStage
from ecs.conditions.player import SteppedOn
from gamemap import GameMap, Dungeon
from systems import RenderSystem, MovementSystem, LightingSystem, TriggerSystem
from engine import Engine

SCREEN_WIDTH = 81
SCREEN_HEIGHT = 51
LIMIT_FPS = 20

def getInput():
    user_input = tdl.event.key_wait()

    if user_input.key == 'ENTER' and user_input.alt:
        #Alt+Enter: toggle fullscreen
        tdl.set_fullscreen(not tdl.get_fullscreen())
    elif user_input.key == 'ESCAPE':
        return False  #exit game

    return user_input

    
tdl.set_font('dundalk12x12_gs_tc.png', greyscale=True, altLayout=True)
console = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Roguelike", fullscreen=False)

engine = Engine()

gamemap = GameMap(81, 51, stageIndex = 0)
dungeon = Dungeon(gamemap, 
    density = 10000, twistiness = 80, connectivity = 8, 
    minRoomSize = 2, maxRoomSize = 5
)
dungeon.generate()
startx, starty = dungeon.randomPosition()
exitx, exity = dungeon.randomPosition()
stairsdown = Entity()
stairsdown.addComponent('position', Position(x=startx+1, y=starty+1, stage=0))
stairsdown.addComponent('appearance', Appearance('stairs', bgcolor=(130, 85, 50), layer=1))
stairsdown.addComponent('physical', Physical(blocks_sight = False, blocked = False))
stairsTrigger = Trigger(
    action = MoveStage(engine, direction = 1),
    condition = SteppedOn()
)
stairsdown.addComponent('trigger', stairsTrigger)
engine.addEntity(stairsdown)



engine.addStage(0, gamemap)
gamemap = GameMap(81, 51, stageIndex = 1)
dungeon = Dungeon(gamemap, 
    density = 100, twistiness = 20, connectivity = 20, 
    minRoomSize = 2, maxRoomSize = 10
)
dungeon.generate()


engine.addStage(1, gamemap)
engine.setStage(0)

player = Entity()
engine.addEntity(player)
engine.addComponentToEntity(player.uid, 'position', Position(x=startx, y=starty, stage=0))
engine.addComponentToEntity(player.uid, 'appearance', Appearance('player', fgcolor=(255,255,255), character='@', layer=1))
engine.addComponentToEntity(player.uid, 'physical', Physical(visible=True, blocked = True))
engine.addComponentToEntity(player.uid, 'player', Player())
engine.addComponentToEntity(player.uid, 'controllable', {})
engine.addComponentToEntity(player.uid, 'moveable', {})
engine.addComponentToEntity(player.uid, 'light_source', LightSource(radius=8, tint=(20, 20, 5), strength=2.5))
goblin = Entity()
engine.addEntity(goblin)
engine.addComponentToEntity(goblin.uid, 'position', Position(x=10, y=10, stage=0))
engine.addComponentToEntity(goblin.uid, 'appearance', Appearance('goblin', fgcolor=(0,255,0), character='G', layer=1))
engine.addComponentToEntity(goblin.uid, 'physical', Physical(visible=False, blocked = True))
engine.addComponentToEntity(goblin.uid, 'moveable', {})

show_map = False
render = RenderSystem()
move = MovementSystem()
triggers = TriggerSystem()
light = LightingSystem()
light(engine)
render(engine, console, recompute_fov = True)


renderTimes = []
while not tdl.event.is_window_closed():
    keys = getInput()
    exit_game = not keys

    if exit_game:
        break

    start = datetime.datetime.now()
    if keys.key == 'TEXT' and keys.text == '§':
        engine.getStage().noFOW = not engine.getStage().noFOW

    recompute_fov = move(keys, engine, console)
    triggers(engine, console)

    if recompute_fov:
        light(engine)

    render(engine, console, recompute_fov=recompute_fov)
    end = datetime.datetime.now()
    diff = end - start
    renderTimes.append(diff.microseconds)
    start = datetime.datetime.now()

avgRenderTime = sum(renderTimes) / len(renderTimes)
print("Average render time: %f" % (avgRenderTime))


