import tdl
import tcod as libtcodpy
from random import randint

from entities import Entity
from gamemap import GameMap, Dungeon

SCREEN_WIDTH = 81
SCREEN_HEIGHT = 51
LIMIT_FPS = 20

def renderEntites(console):
    for entity in entities:
        entity.draw(console)
    tdl.flush()
    for entity in entities:
        entity.clear(console)

def handleInput():
    global show_map

    dx = 0
    dy = 0

    user_input = tdl.event.key_wait()

    if user_input.key == 'TEXT' and user_input.text == '§':
        show_map ^= True

    if user_input.key == 'UP':
        dy -= 1 
        fov_recompute = True
    elif user_input.key == 'DOWN':
        dy += 1
        fov_recompute = True
    elif user_input.key == 'LEFT':
        dx -= 1
        fov_recompute = True
    elif user_input.key == 'RIGHT':
        dx += 1
        fov_recompute = True

    if user_input.key == 'ENTER' and user_input.alt:
        #Alt+Enter: toggle fullscreen
        tdl.set_fullscreen(not tdl.get_fullscreen())
    elif user_input.key == 'ESCAPE':
        return True  #exit game

    playerx = player.x + dx
    playery = player.y + dy
    if gamemap.is_blocked(playerx, playery) == False:
        player.move(dx, dy)

    return False
    
tdl.set_font('dundalk12x12_gs_tc.png', greyscale=True, altLayout=True)
console = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Roguelike", fullscreen=False)
gamemap = GameMap(81, 51)
dungeon = Dungeon(gamemap, 
    density = 10000, twistiness = 80, connectivity = 8, 
    minRoomSize = 2, maxRoomSize = 5
)
dungeon.generate()
entities = []

startx, starty = dungeon.startPosition()
player = Entity(startx, starty, '@', (255,255,255))
npc = Entity(10, 10, 'N', (255,0,0))
entities.append(player)
entities.append(npc)

show_map = False
gamemap.computeFOV(player.x, player.y)
gamemap.render(console, noFOW=show_map)
renderEntites(console)

while not tdl.event.is_window_closed():
    exit_game = handleInput()

    fov_recompute = True
    if fov_recompute:
        gamemap.computeFOV(player.x, player.y)
        fov_recompute = False

    print(show_map)
    gamemap.render(console, noFOW=show_map)
    renderEntites(console)
    if exit_game:
        break




