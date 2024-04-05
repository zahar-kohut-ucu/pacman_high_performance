# Maze implementation
# Imports
from creatures import Ghost, Pacman
import node
import random


class Maze:
    def __init__(self, m: int = 35, n: int = 35, ghostsAmount = 0, numberOfDots: int = 1000000000000, numberOfBroken = 52, setSeed: bool = False, seed: int = 100):
        if setSeed:
            random.seed(seed)
        self.m = m
        self.n = n
        self.trueM = m
        self.trueN = n * 2 + 1
        self.ghostsAmount = ghostsAmount
        self.numberOfDots = numberOfDots
        self._maze = [[node.Node(i, j, 0, node.nodeStates.wallState) for j in range(n)] for i in range(m)]
        self._freePositions = []
        self._dotsPosition = []
        self._ghostsPosition1 = []
        self._ghostsPosition2 = []
        self._pacmansPositions = []
        # generate maze
        self.generateMaze(self.getNode(random.randint(0, m - 1), self.n - 1))
        self.breakWalls(numberOfBroken)
        self.spawnDots()
        self.mazeExtend()
        # self.wallExtend()

    def getDotsPosition(self):
        return self._dotsPosition

    def getFreePosition(self):
        return self._freePosition

    def clearGhostPositions(self):
        self._ghostsPosition1 = []
        self._ghostsPosition2 = []

    def getGhostPositions(self, team: int) -> list[int]:
        if team == 1:
            return self._ghostsPosition1
        if team == 2:
            return self._ghostsPosition2

    def getNode(self, i: int, j: int):
        return self._maze[i][j]

    def getNeighbours(self, current: node.Node):
        i, j = current._x, current._y
        hor = list(filter(lambda item: 0 <= item < self.n, [j - 2, j + 2]))
        ver = list(filter(lambda item: 0 <= item < self.m, [i - 2, i + 2]))
        return [self.getNode(i, item) for item in hor] + [self.getNode(item, j) for item in ver]

    # maze generator using DFS
    def generateMaze(self, current: node.Node):
        # getting neighbours
        current.changeState(2)
        self._freePositions.append(current.getCoordinates())
        neighbours = self.getNeighbours(current)
        random.shuffle(neighbours)
        for neighbor in neighbours:
            if isinstance(neighbor.getState(), node.nodeStates.wallState):
                breakWallAt = (int((current.getCoordinates()[0] + neighbor.getCoordinates()[0])/2), int((current.getCoordinates()[1] + neighbor.getCoordinates()[1])/2))
                self._freePositions.append(breakWallAt)
                self.getNode(breakWallAt[0], breakWallAt[1]).changeState(2)
                self.generateMaze(neighbor)
    
    
    def breakWalls(self, n: int):
        go = n
        checked = set()
        while go:
            i, j = random.randint(1, self.m - 2), random.randint(1, self.n - 2)
            if str(self.getNode(i, j).getState()) == "wall":
                up = str(self.getNode(i + 1, j).getState()) == "wall"
                down = str(self.getNode(i - 1, j).getState()) == "wall"
                left = str(self.getNode(i, j - 1).getState()) == "wall"
                right = str(self.getNode(i, j + 1).getState()) == "wall"
                if ((up and down) and not (left or right)) or ((left and right) and not (up or down)):
                    self.getNode(i, j).changeState(2)
                    self._freePositions.append((i, j))
                    go -= 1
            

    def breakWalls(self, n: int):
        go = n
        checked = set()
        while go:
            i, j = random.randint(1, self.m - 2), random.randint(1, self.n - 2)
            if str(self.getNode(i, j).getState()) == "wall":
                up = str(self.getNode(i + 1, j).getState()) == "wall"
                down = str(self.getNode(i - 1, j).getState()) == "wall"
                left = str(self.getNode(i, j - 1).getState()) == "wall"
                right = str(self.getNode(i, j + 1).getState()) == "wall"
                if ((up and down) and not (left or right)) or ((left and right) and not (up or down)):
                    self.getNode(i, j).changeState(2)
                    self._freePositions.append((i, j))
                    go -= 1
            
    def spawnDots(self, n: int = 0, team: int = 1):
        if n == 0:
            n = self.numberOfDots
        if self._dotsPosition == []:
            self._dotsPosition = random.sample(self._freePositions, min(len(self._freePositions), n))
            for i, j in self._dotsPosition:
                self.getNode(i, j).changeState(3)
                self.getNode(i, j)._team = team
        else:
            choice = random.choice(self._freePositions)
            while self.getNode(*choice).isTaken():
                choice = random.choice(self._freePositions)

            self._dotsPosition.append(choice)
            self._freePositions.remove(choice)
            self.getNode(*choice).changeState(3)
            self.getNode(*choice)._team = team




    def mazeExtend(self):
        for i in range(self.m):
            self._maze[i].append(node.Node(i, self.n, 0, node.nodeStates.freeState))
            self._maze[i] += [node.Node(i, self.n + 1 + j, 0, self.getNode(i, -(j + 2)).getStateClass()) for j in range(self.n)]
        length = len(self._freePositions)
        for i in range(length):
            x, y = self._freePositions[i]
            self._freePositions.append((x, self.trueN - y - 1))

        arr = []
        for i, j in self._dotsPosition:
            arr.append((i, self.trueN - j - 1))
            self.getNode(i, self.trueN - j - 1)._team = 2
        self._dotsPosition += arr

    def spawnPacmans(self, pacmans: list[Pacman]):
        for i in range(self.trueN):
            for j in range(self.trueM):
                if j <= self.trueN//4:
                    if str(self.getNode(i, j).getState()) == "free":
                        for pacman in pacmans:
                            if pacman.getTeam() == 2:
                                j = self.trueN - j - 1
                            self.getNode(i, j).placeCreatue(pacman)
                            pacman.move(i, j)
                        return None

    def spawnGhosts(self, ghosts: list[Ghost]):
        self.clearGhostPositions()
        length = len(self.getDotsPosition())//2
        for k, (i, j) in enumerate(self.getDotsPosition()[:self.ghostsAmount]):
            coords = [[i,j+1], [i+1,j], [i,j-1], [i-1,j]]
            for x, y in coords:
                if 0 <= x < self.trueM and 0 <= y < self.trueN and str(self.getNode(x, y).getState()) == "free":
                    ghosts[k + self.ghostsAmount].move(x,self.trueN - y - 1)
                    self._ghostsPosition2.append((x,self.trueN - y - 1))
                    self.getNode(x, self.trueN - y - 1).placeCreatue(ghosts[k + self.ghostsAmount])
                    ghosts[k].move(x,y)
                    self._ghostsPosition1.append((x,y))
                    self.getNode(x, y).placeCreatue(ghosts[k])
                    break

    def changeGhostsCoordinates(self, ghosts: list[Ghost], newCoordsGh: list[int]):
        self.clearGhostPositions()
        for k, ghost in enumerate(ghosts):
            i, j = ghost.getCoordinates()
            if not self.checkDot(i, j):
                self.getNode(i, j).setFree()
            if not self.checkDot(*newCoordsGh[k]):
                self.getNode(*newCoordsGh[k]).placeCreatue(ghost)
            ghost.move(*newCoordsGh[k])
            if ghost.getTeam() == 1:
                self._ghostsPosition1.append(newCoordsGh[k])
            else:
                self._ghostsPosition2.append(newCoordsGh[k])

    def changePacmansCoordinates(self, pacmans: list[Pacman], newCoordsPac: list[int]):
        for k, pacman in enumerate(pacmans):
            i, j = pacman.getCoordinates()
            if not self.checkDot(i, j):
                self.getNode(i, j).setFree()
            if not self.checkDot(*newCoordsPac[k]):
                self.getNode(*newCoordsPac[k]).placeCreatue(pacman)
            pacman.move(*newCoordsPac[k])

    def checkDot(self, x: int, y: int):
        return (x, y) in self._dotsPosition


    def eatAndRespawnDot(self, pacman: Pacman):
        x, y  = pacman.getCoordinates()
        self.getNode(x, y).setFree()
        self.getNode(x, y).changeState(2)
        pacman.addPoint()
        self._dotsPosition.remove((x,y))
        # self.spawnDots(1, 3 - pacman.getTeam())
        # self._freePositions.append((x,y))


    def checkMove(self, pacman: Pacman):
        # print(pacman.getPoints())
        # print(self.numberOfDots)
        if pacman.getCoordinates() in self.getGhostPositions(3 - pacman.getTeam()):
            return 0
        if pacman.getCoordinates() in self.getDotsPosition() and pacman.getTeam() != self.getNode(*pacman.getCoordinates()).getTeam():
            return 1
        return 2
