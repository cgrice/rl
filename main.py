import tdl
import tcod as libtcodpy
from random import randint

from ecs import Entity
from gamemap import GameMap, Dungeon
from components import Position, Appearance, Player, Physical, LightSource
from systems import RenderSystem, MovementSystem, LightingSystem
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
engine.addStage(0, gamemap)
gamemap = GameMap(81, 51, stageIndex = 1)
dungeon = Dungeon(gamemap, 
    density = 100, twistiness = 20, connectivity = 20, 
    minRoomSize = 2, maxRoomSize = 10
)
dungeon.generate()
startx, starty = dungeon.startPosition()
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
light = LightingSystem()
light(engine)
render(engine, console, recompute_fov = True)


while not tdl.event.is_window_closed():
    keys = getInput()
    exit_game = not keys

    if exit_game:
        break

    if keys.key == 'TEXT' and keys.text == '§':
        gamemap.noFOW = not gamemap.noFOW

    recompute_fov = move(keys, engine, console)

    if keys.key == 'TEXT' and keys.text == '=':
        nextIndex = engine.stageIndex + 1
        if engine.hasStage(nextIndex):
            engine.setStage(nextIndex)
            recompute_fov = True
            console.clear()
            position = engine.getEntity(player.uid).getComponent('position')
            position.stage = nextIndex
            player.addComponent('position', position)

    if keys.key == 'TEXT' and keys.text == '-':
        nextIndex = engine.stageIndex - 1
        if engine.hasStage(nextIndex):
            engine.setStage(nextIndex)
            recompute_fov = True
            console.clear()
            position = engine.getEntity(player.uid).getComponent('position')
            position.stage = nextIndex
            player.addComponent('position', position)

    if recompute_fov:
        light(engine)

    render(engine, console, recompute_fov=recompute_fov)




