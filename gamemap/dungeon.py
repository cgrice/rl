from random import randint, choice
import sys

from .rect import Rect

class Dungeon:

    

    def __init__(self, gamemap):
        self.rooms = []
        self.map = gamemap
        self.regions = [[-1 for x in range(gamemap.width)] for y in range(gamemap.height)] 
        self.currentRegion = -1
        self.directions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ]
        self.color = (100, 100, 250)

    def generate(self):
        self._fillMap()
        self._addRooms(1000)
        self._addMaze()

        # self._removeDeadEnds()

    def overlaps(self, room):
        overlaps = False
        for other in self.rooms:
            if room.intersects(other):
                overlaps = True

        return overlaps

    def startPosition(self):
        x, y = self._randomPosition()
        while self.map.in_bounds(x, y) == False:
            x, y = self._randomPosition()

        return (x, y)

    def _addRooms(self, numRooms):
        for i in range(numRooms):
            room = self._generateRoom()
            
            if self.overlaps(room) == True:
                continue

            self.rooms.append(room)

        for room in self.rooms:
            self._startRegion()
            self._carveRoom(room)

    def _generateRoom(self):
        size = randint(1, 3) * 2 + 1
        rectangularity = randint(0, 1 + size // 2) * 2
        w = size
        h = size

        if(randint(0, 1) > 0):
            w = w + rectangularity
        else:
            h = h + rectangularity

        x = randint(0, (self.map.width - w - 1) // 2) * 2 + 1
        y = randint(0, (self.map.height - h - 1) // 2) * 2 + 1

        room = Rect(x, y, w, h)
        return room

    def _addMaze(self):
        for y in range(1, self.map.height - 1, 2):
            for x in range(1, self.map.width - 1, 2):
                if self.map.is_blocked(x, y) == False:
                    continue
                self._growMaze(x, y)

    def _growMaze(self, x, y):
        cells = []
        lastdir = None

        self._startRegion()
        self._carve(x, y)

        cells.append((x, y))

        while len(cells) > 0:
            x, y = cells[-1]
            unmadeCells = []

            for direction in self.directions:
                dx, dy = direction
                
                if self._canCarve(x, y, dx, dy):
                    unmadeCells.append((dx, dy))

            if len(unmadeCells) > 0:
                if lastdir in unmadeCells and randint(1, 100) < 0:
                    direction = lastdir
                else:
                    direction = choice(unmadeCells)

                dx, dy = direction
                lastdir = direction

                self._carve(x + dx, y + dy)
                self._carve(x + dx*2, y + dy*2)
                cells.append((x + dx*2, y + dy*2))
            else:
                cells.pop()
                lastdir = None
            


    def _carveRoom(self, room):
        for x in range(room.x1, room.x2):
            for y in range(room.y1, room.y2):
                try:
                    self._carve(x, y)
                except:
                    continue

    def _fillMap(self):
        for x, row in enumerate(self.map.tiles):
            for y, tile in enumerate(row):
                self.map[x][y].blocks_sight = True
                self.map[x][y].blocked = True

    def _carve(self, x, y):
        self.map[x][y].blocks_sight = False
        self.map[x][y].blocked = False
        self.map[x][y].color = self.color

    def _canCarve(self, x, y, dx, dy):
        pos1 = (x + dx, y + dy)
        pos2 = (x + (dx*2), y + (dy*2))

        if self.map.in_bounds(pos1[0], pos1[1]) == False or \
           self.map.in_bounds(pos2[0], pos2[1]) == False:
            return False

        return self.map.is_blocked(pos1[0], pos1[1]) \
           and self.map.is_blocked(pos2[0], pos2[1]) 

    def _randomRoom(self):
        return choice(self.rooms)

    def _randomPosition(self):
        room = self._randomRoom()
        return room.center()

    def _startRegion(self):
        self.currentRegion += 1
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))

    def _removeDeadEnds(self):
        done = False

        while done == False:
            done = True

            for x in range(0, self.map.width):
                for y in range(0, self.map.height):
                    if self.map.is_blocked(x, y): 
                        continue

                    exits = 0
                    # If it only has one exit, it's a dead end.
                    for direction in self.directions:
                        dx, dy = direction
                        if self.map.is_blocked(x + dx, y + dy) == False:
                            exits = exits + 1

                    if exits <= 1: 
                        done = False
                        self.map[x][y].blocked = True
                        self.map[x][y].blocks_sight = True
