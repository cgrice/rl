from explorer.gamemap.tiles.map import WALL_STONE, GROUND_STONE, GROUND_DIRT, \
    WALL_DIRT_DARK, GROUND_GRASS, \
    STAIRS_STONE_DOWN_RIGHT, STAIRS_STONE_UP_LEFT

STANDARD_DUNGEON = {
    'wall-color': (255, 100, 100, 100),
    'ground-color': (255, 0, 0, 0),
    'tiles': {
        'wall': [' '],
        'ground': GROUND_STONE,
        'stairs-down': STAIRS_STONE_DOWN_RIGHT,
        'stairs-up': STAIRS_STONE_UP_LEFT,
    }
}

GRASS_DUNGEON = {
    'wall-color': (255, 100, 100, 100),
    'ground-color': (255, 48, 43, 26),
    'tiles': {
        'wall': WALL_DIRT_DARK,
        'ground': GROUND_GRASS,
        'stairs-down': STAIRS_STONE_DOWN_RIGHT,
        'stairs-up': STAIRS_STONE_UP_LEFT,
    }
}