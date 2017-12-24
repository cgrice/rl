import tdl
from entity import Entity

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20

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
        return True, (dx, dy)  #exit game

    return False, (dx, dy)
    
tdl.set_font('dundalk12x12_gs_tc.png', greyscale=True, altLayout=True)
console = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Roguelike", fullscreen=False)
entities = []
player = Entity(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, '@', (255,255,255))
npc = Entity(10, 10, 'N', (255,0,0))
entities.append(player)
entities.append(npc)

renderEntites(console)

while not tdl.event.is_window_closed():
    exit_game, delta = handleInput()
    player.move(*delta)
    renderEntites(console)
    if exit_game:
        break




