# Maze implementation
# Imports
#from creatures import Ghost, Pacman
import random
import numpy as np

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

        self.lengths = np.zeros(5,dtype=int)
        self.freePositions = np.empty((self.trueM*self.trueN, 2), dtype=int)
        self.dotsPosition = np.empty((numberOfDots*2, 2), dtype=int)
        self.ghostsPosition1 = np.empty((m*n, 2))
        self.ghostsPosition2 = np.empty((m*n, 2))
        self.pacmansPositions = np.empty((m*n, 2))
        
        # generate maze
        self.generateMaze(random.randint(0, m - 1), self.n - 1)
        self.breakWalls(numberOfBroken)
        self.spawnDots(self.numberOfDots)
        self.mazeExtend()

    def clearGhostPositions(self):
        self.ghostsPosition1 = np.empty((self.m*self.n, 2))
        self.ghostsPosition2 = np.empty((self.m*self.n, 2))

    def generateMaze(self, i, j):
        self.maze[i][j] = 0
        self.freePositions[self.lengths[0]] = np.array([i, j])
        self.lengths[0] += 1
        neighbours = list(filter(lambda nei: 0 <= nei[0] < self.m and 0 <= nei[1] < self.n, [(i + 2, j), (i - 2, j), (i, j + 2), (i, j - 2)]))
        random.shuffle(neighbours)
        for ni, nj in neighbours:
            if self.maze[ni][nj] == 1:
                bi, bj = int((i + ni)/2), int((j + nj)/2)
                self.freePositions[self.lengths[0]] = np.array([bi, bj])
                self.lengths[0] += 1
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
                    self.freePositions[self.lengths[0]] = np.array([i, j])
                    self.lengths[0] += 1
                    go -= 1
            
        
    def spawnDots(self, n: int, team: int = 1):
            self.lengths[1] = min(self.lengths[0], n)
            indices = np.random.choice(self.lengths[0], self.lengths[1], replace = False)
            self.dotsPosition[:self.lengths[1]] = self.freePositions[indices]
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
        length = self.lengths[0]
        for ind in range(length):
            i, j = self.freePositions[ind]
            self.freePositions[self.lengths[0]] = np.array([i, self.trueN - j - 1])
            self.lengths[0] += 1

        length = self.lengths[1]
        for ind in range(length):
            i, j = self.dotsPosition[ind]
            self.dotsPosition[self.lengths[1]] = np.array([i, self.trueN - j - 1])
            self.lengths[1] += 1

    # def spawnPacmans(self, pacmans: list[Pacman]):
    #     for i in range(self.trueN):
    #         for j in range(self.trueM):
    #             if j <= self.trueN//4:
    #                 if str(self.getNode(i, j).getState()) == "free":
    #                     for pacman in pacmans:
    #                         if pacman.getTeam() == 2:
    #                             j = self.trueN - j - 1
    #                         self.getNode(i, j).placeCreatue(pacman)
    #                         pacman.move(i, j)
    #                     return None

    # def spawnGhosts(self, ghosts: list[Ghost]):
    #     self.clearGhostPositions()
    #     length = len(self.getDotsPosition())//2
    #     for k, (i, j) in enumerate(self.getDotsPosition()[:self.ghostsAmount]):
    #         coords = [[i,j+1], [i+1,j], [i,j-1], [i-1,j]]
    #         for x, y in coords:
    #             if 0 <= x < self.trueM and 0 <= y < self.trueN and str(self.getNode(x, y).getState()) == "free":
    #                 ghosts[k + self.ghostsAmount].move(x,self.trueN - y - 1)
    #                 self._ghostsPosition2.append((x,self.trueN - y - 1))
    #                 self.getNode(x, self.trueN - y - 1).placeCreatue(ghosts[k + self.ghostsAmount])
    #                 ghosts[k].move(x,y)
    #                 self._ghostsPosition1.append((x,y))
    #                 self.getNode(x, y).placeCreatue(ghosts[k])
    #                 break

    # def changeGhostsCoordinates(self, ghosts: list[Ghost], newCoordsGh: list[int]):
    #     self.clearGhostPositions()
    #     for k, ghost in enumerate(ghosts):
    #         i, j = ghost.getCoordinates()
    #         if not self.checkDot(i, j):
    #             self.getNode(i, j).setFree()
    #         if not self.checkDot(*newCoordsGh[k]):
    #             self.getNode(*newCoordsGh[k]).placeCreatue(ghost)
    #         ghost.move(*newCoordsGh[k])
    #         if ghost.getTeam() == 1:
    #             self._ghostsPosition1.append(newCoordsGh[k])
    #         else:
    #             self._ghostsPosition2.append(newCoordsGh[k])

    # def changePacmansCoordinates(self, pacmans: list[Pacman], newCoordsPac: list[int]):
    #     for k, pacman in enumerate(pacmans):
    #         i, j = pacman.getCoordinates()
    #         if not self.checkDot(i, j):
    #             self.getNode(i, j).setFree()
    #         if not self.checkDot(*newCoordsPac[k]):
    #             self.getNode(*newCoordsPac[k]).placeCreatue(pacman)
    #         pacman.move(*newCoordsPac[k])

    # def checkDot(self, x: int, y: int):
    #     return (x, y) in self._dotsPosition


    # def eatAndRespawnDot(self, pacman: Pacman):
    #     x, y  = pacman.getCoordinates()
    #     self.getNode(x, y).setFree()
    #     self.getNode(x, y).changeState(2)
    #     pacman.addPoint()
    #     self._dotsPosition.remove((x,y))
    #     # self.spawnDots(1, 3 - pacman.getTeam())
    #     # self._freePositions.append((x,y))


    # def checkMove(self, pacman: Pacman):
    #     # print(pacman.getPoints())
    #     # print(self.numberOfDots)
    #     if pacman.getCoordinates() in self.getGhostPositions(3 - pacman.getTeam()):
    #         return 0
    #     if pacman.getCoordinates() in self.getDotsPosition() and pacman.getTeam() != self.getNode(*pacman.getCoordinates()).getTeam():
    #         return 1
    #     return 2
