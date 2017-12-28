from random import randint, choice
import sys
import math

from .rect import Rect

class Dungeon:

    def __init__(self, gamemap, 
        twistiness = 50, density = 10, connectivity = 5,
        minRoomSize = 1, maxRoomSize = 3
    ):
        self.rooms = []
        self.map = gamemap
        self.regions = [[-1 for y in range(gamemap.height)] for x in range(gamemap.width)] 
        self.currentRegion = -1
        self.directions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ]
        self.color = (50, 50, 150)
        self.twistiness = twistiness
        self.density = density
        self.connectivity = 100 - connectivity
        self.minRoomSize = minRoomSize
        self.maxRoomSize = maxRoomSize

    def generate(self):
        self._fillMap()
        self._addRooms(self.density)
        self._addMaze()
        self._connectRegions()
        self._removeDeadEnds()

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
        size = randint(self.minRoomSize, self.maxRoomSize) * 2 + 1
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
                if lastdir in unmadeCells and randint(0, 100) > self.twistiness:
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
                self.map[x][y] = self.map.createWall(x, y)

    def _carve(self, x, y):
        floor = self.map.createFloor(x, y)
        self.map[x][y] = floor
        self.regions[x][y] = self.currentRegion

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

    def _connectRegions(self):
        connectorRegions = {}

        for x in range(0, self.map.width + 1):
            for y in range(0, self.map.height + 1):
                # If it's already carved, ignore it
                if self.map.is_blocked(x, y) == False:
                    continue

                # Check for regions in all directions
                regions = set()
                for direction in self.directions:
                    dx, dy = direction
                    try:
                        region = self.regions[x+dx][y+dy]
                        if region != -1:
                            regions.add(region)
                    except:
                        continue

                # If this position doesn't connect at least 2 regions, it's not
                # a potential connector, so discard it
                if len(regions) < 2: continue

                connectorRegions[(x, y)] = regions

        connectors = list(connectorRegions.keys())

        # Create a dict to track which regions have been merged
        merged = {}
        openRegions = set()
        for i in range(0, self.currentRegion + 1):
            
            merged[i] = i
            openRegions.add(i)

        

        while len(openRegions) >= 1:
            connector = choice(connectors)

            self._carveConnector(*connector)

            regions = list(map(
                lambda region: merged[region], 
                connectorRegions[connector]
            ))
            dest = regions[0]
            sources = regions[1:]

            for i in range(0, self.currentRegion + 1):
                if merged[i] in sources:
                    merged[i] = dest

            for source in sources:
                try:
                    openRegions.remove(source)
                except:
                    pass

            for pos in connectors:
                if self._distance(connector, pos) < 2:
                    connectors.remove(pos)
                    continue

                regions = set(list(map(
                    lambda region: merged[region],
                    connectorRegions[pos] 
                )))

                if len(regions) > 1:
                    continue

                if randint(0, 100) > self.connectivity:
                    self._carveConnector(*pos)
                
                connectors.remove(pos)

    def _carveConnector(self, x, y):
        if randint(0, 100) > 500:
            connector = self.map.createDoor(x, y)
        else:
            connector = self.map.createFloor(x, y)
        self.map[x][y] = connector
        self.regions[x][y] = self.currentRegion

    def _startRegion(self):
        self.currentRegion += 1

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
                        wall = self.map.createWall(x, y)
                        self.map[x][y] = wall

    def _distance(self, p0, p1):
        return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)