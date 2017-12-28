import tdl
import tcod as libtcodpy
from random import randint

from ecs import Entity
from gamemap import GameMap, Dungeon
from components import Position, Appearance, Player, Physical, LightSource
from systems import RenderSystem, MovementSystem, LightingSystem

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
gamemap = GameMap(81, 51)
dungeon = Dungeon(gamemap, 
    density = 10000, twistiness = 80, connectivity = 8, 
    minRoomSize = 2, maxRoomSize = 5
)


tiles = dungeon.generate()
startx, starty = dungeon.startPosition()
player = Entity()
player.addComponent('position', Position(x=startx, y=starty))
player.addComponent('appearance', Appearance('player', fgcolor=(255,255,255), character='@', layer=1))
player.addComponent('physical', Physical(visible=True, blocked = True))
player.addComponent('player', Player())
player.addComponent('controllable', {})
player.addComponent('moveable', {})
player.addComponent('light_source', LightSource(radius=8, tint=(15, 20, 5), strength=2.5))
goblin = Entity()
goblin.addComponent('position', Position(x=10, y=10))
goblin.addComponent('appearance', Appearance('player', fgcolor=(0,255,0), character='G', layer=1))
goblin.addComponent('physical', Physical(visible=False, blocked = True))
goblin.addComponent('moveable', {})
entities = []
entities.append(player)
entities.append(goblin)

show_map = False
render = RenderSystem()
move = MovementSystem()
light = LightingSystem()
light(entities, gamemap)
render(entities, gamemap, console, recompute_fov = True)


while not tdl.event.is_window_closed():
    keys = getInput()
    exit_game = not keys

    if exit_game:
        break

    if keys.key == 'TEXT' and keys.text == '§':
        gamemap.noFOW = not gamemap.noFOW


    recompute_fov = move(keys, entities, gamemap, console)
    if recompute_fov:
        light(entities, gamemap)
    render(entities, gamemap, console, recompute_fov=recompute_fov)




