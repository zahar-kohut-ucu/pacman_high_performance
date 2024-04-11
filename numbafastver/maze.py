# Maze implementation
# Imports
#from creatures import Ghost, Pacman
import random
import numpy as np
import copy

# 0 - free, 1 - wall, 2 - red dot, 3 - yellow dot

class Maze:
    def __init__(self, m: int = 35, n: int = 35, ghostsAmount = 0, numberOfDots: int = 8, numberOfBroken = 52, setSeed: bool = False, seed: int = 100):
        if setSeed:
            random.seed(seed)
        self.m = m
        self.n = n
        self.trueM = m
        self.trueN = n * 2 + 1
        self.ghostsAmount = ghostsAmount
        self.numberOfDots = numberOfDots

        self.maze = np.ones((n,m), dtype=int)

        self.freePositions = set()

        self.redDotsPosition = set()
        self.yellowDotsPosition = set()
        self.dotsPosition = set()

        self.ghostsPosition1 = set()
        self.ghostsPosition2 = set()
        self.pacmansPositions = set()
        
        # generate maze
        self.generateMaze(random.randint(0, m - 1), self.n - 1)
        self.breakWalls(numberOfBroken)
        self.spawnDots(self.numberOfDots)
        self.mazeExtend()

    def generateMaze(self, i, j):
        self.maze[i][j] = 0
        self.freePositions.add((i, j))
        neighbours = list(filter(lambda nei: 0 <= nei[0] < self.m and 0 <= nei[1] < self.n, [(i + 2, j), (i - 2, j), (i, j + 2), (i, j - 2)]))
        random.shuffle(neighbours)
        for ni, nj in neighbours:
            if self.maze[ni][nj] == 1:
                bi, bj = int((i + ni)/2), int((j + nj)/2)
                self.freePositions.add((bi, bj))
                self.maze[bi][bj] = 0
                self.generateMaze(ni, nj)
    
    def breakWalls(self, n: int):
        go = n
        while go:
            i, j = random.randint(1, self.m - 2), random.randint(1, self.n - 2)
            if self.maze[i][j] == 1:
                up = self.maze[i + 1][j]
                down = self.maze[i - 1][j] == 1
                left = self.maze[i][j - 1] == 1
                right = self.maze[i][j + 1] == 1
                if ((up and down) and not (left or right)) or ((left and right) and not (up or down)):
                    self.maze[i][j] = 0
                    self.freePositions.add((i, j))
                    go -= 1
            
        
    def spawnDots(self, n: int):
            self.redDotsPosition = set(random.sample(self.freePositions, min(len(self.freePositions), n)))
            self.dotsPosition = copy.copy(self.redDotsPosition)
            for i, j in self.dotsPosition:
                self.maze[i][j] = 2

    def mazeExtend(self):
        newMaze = np.empty((self.trueM, self.trueN), dtype=int)
        for i in range(self.m):
            add_zero = np.append(self.maze[i], 0)
            rightPart = np.array(add_zero[:-1][::-1])
            rightPart[rightPart == 2] = 3
            newMaze[i] = np.append(add_zero, rightPart)
            
        self.maze = newMaze

        tempFree = copy.copy(self.freePositions)
        for i, j in tempFree:
            self.freePositions.add((i, self.trueN - j - 1))

        tempDots = copy.copy(self.dotsPosition)
        for i, j in tempDots:
            self.yellowDotsPosition.add((i, self.trueN - j - 1))
            self.dotsPosition.add((i, self.trueN - j - 1))
       
    def spawnPacmans(self, pacmans):
        for i in range(self.trueN):
            for j in range(self.trueM):
                if j <= self.trueN//4 and self.maze[i][j] == 0:
                        pacmans[0][0], pacmans[0][1] = i, j
                        pacmans[1][0], pacmans[1][1] = i, self.trueN - j - 1
                        self.pacmansPositions.add((i, j))    
                        self.pacmansPositions.add((i, self.trueN - j - 1))    
                        return None

    def spawnGhosts(self, ghosts):
        for ind, positions in enumerate([self.redDotsPosition, self.yellowDotsPosition]):
            counter = self.ghostsAmount
            for k, (i, j) in enumerate(positions):
                if not counter:
                    break 
                coords = [(i,j+1), (i+1,j), (i,j-1), (i-1,j)]
                for x, y in coords:
                    if 0 <= x < self.trueM and 0 <= y < self.trueN and self.maze[x][y] in [0,2,3]:
                        ghosts[k + ind*self.ghostsAmount][0], ghosts[k + ind*self.ghostsAmount][1] = x, y
                        if ind:
                            self.ghostsPosition2.add((x, y))
                        else:
                            self.ghostsPosition1.add((x, y))
                        counter -= 1
                        break

    def clearGhostPositions(self):
        self.ghostsPosition1.clear()
        self.ghostsPosition2.clear()

    def changeGhostsCoordinates(self, ghosts, newCoordsGh):
        self.clearGhostPositions()
        for k, ghost in enumerate(ghosts):
            i, j = ghost[0], ghost[1]
            ghost[0], ghost[1] = newCoordsGh[k][0], newCoordsGh[k][1]
            if ghost[2] == 1:
                self.ghostsPosition1.add(newCoordsGh[k])
            else:
                self.ghostsPosition2.add(newCoordsGh[k])

    def changePacmansCoordinates(self, pacmans, newCoordsPac):
        for k, pacman in enumerate(pacmans):
            pacman[0], pacman[1] = newCoordsPac[k][0], newCoordsPac[k][1]

    def checkDot(self, x: int, y: int):
        return (x, y) in self.dotsPosition

    def eatAndRespawnDot(self, pacman):
        i, j  = pacman[0], pacman[1]
        self.maze[i][j] = 0
        pacman[4] += 1
        if pacman[2] == 1:
            self.yellowDotsPosition.remove((i, j))
        else:
            self.redDotsPosition.remove((i, j))
        self.dotsPosition.remove((i,j))


    def checkMove(self, pacman):
        ghostPositions = self.ghostsPosition1 if pacman[2] == 2 else self.ghostsPosition2
        dotsPosition = self.yellowDotsPosition if pacman[2] == 1 else self.redDotsPosition
        if (pacman[0], pacman[1]) in ghostPositions:
            pacman[3] = 0
            return 0
        if (pacman[0], pacman[1]) in dotsPosition:
            return 1
        return 2
