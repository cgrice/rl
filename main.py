import tdl
from entities import Entity
from gamemap import GameMap, Dungeon

SCREEN_WIDTH = 100
SCREEN_HEIGHT = 100
LIMIT_FPS = 20

def renderMap(console):
    for y in range(gamemap.height):
        for x in range(gamemap.width):
            wall = gamemap[x][y].blocks_sight
            if wall:
                console.draw_char(x, y, None, fg=None, bg=(10, 10, 10))
            else:
                if gamemap[x][y].color:
                    console.draw_char(x, y, None, fg=None, bg=gamemap[x][y].color)
                else:
                    console.draw_char(x, y, None, fg=None, bg=(50, 50, 150))

def renderEntites(console):
    for entity in entities:
        entity.draw(console)
    tdl.flush()
    for entity in entities:
        entity.clear(console)

def handleInput():
    dx = 0
    dy = 0

    user_input = tdl.event.key_wait()

    if user_input.key == 'UP':
        dy -= 1 
    elif user_input.key == 'DOWN':
        dy += 1
    elif user_input.key == 'LEFT':
        dx -= 1
    elif user_input.key == 'RIGHT':
        dx += 1

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
dungeon = Dungeon(gamemap)
dungeon.generate()
entities = []

startx, starty = dungeon.startPosition()
player = Entity(startx, starty, '@', (255,255,255))
npc = Entity(10, 10, 'N', (255,0,0))
entities.append(player)
entities.append(npc)

renderMap(console)
renderEntites(console)

while not tdl.event.is_window_closed():
    exit_game = handleInput()
    renderMap(console)
    renderEntites(console)
    if exit_game:
        break




