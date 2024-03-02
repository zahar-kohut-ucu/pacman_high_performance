# Maze implementation
# Imports
import node
import random

class Maze:
    def __init__(self, m: int = 35, n: int = 35, numberOfDots: int = 1000000000000, setSeed: bool = False, seed: int = 100):
        if setSeed:
            random.seed(seed)
        self.m = m
        self.n = n
        self.numberOfDots = numberOfDots
        self._maze = [[node.Node(i, j, 1, node.nodeStates.wallState) for j in range(n)] for i in range(m)]
        self._freePositions = []
        self._dotsPosition = []
        # generate maze 
        self.generateMaze(self.getNode(random.randint(0, m - 1), random.randint(0, n - 1)))
        self.spawnDots()
        self.mazeExtend()

    def getDotsPosition(self):
        return self._dotsPosition
    
    def getFreePosition(self):
        return self._freePosition

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
    
    def spawnDots(self):
        self._dotsPosition = random.sample(self._freePositions, min(len(self._freePositions), self.numberOfDots))
        for i, j in self._dotsPosition:
            self.getNode(i, j).changeState(3)

    def mazeExtend(self):
        for i in range(self.m):
            self._maze[i].append(node.Node(i, self.n, 0, node.nodeStates.freeState))
            self._maze[i] += [node.Node(i, self.n + 1 + j, 2, self.getNode(i, -(j + 2)).getStateClass()) for j in range(self.n)]