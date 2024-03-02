# Maze implementation
# Imports
import node
import random

class Maze:
    def __init__(self, m: int = 35, n: int = 35, numberOfDots: int = 4):
        self.m = m
        self.n = n
        self.numberOfDots = numberOfDots
        self._maze = [[node.Node(i, j, 1, node.nodeStates.wallState) for j in range(n)] for i in range(m)]
        self._freePositions = []
        self._dotsPosition = [] 
        self.generateMaze(self.getNode(random.randint(0, m - 1), random.randint(0, n - 1)))
        self.spawnDots()

    def getDotsPosition(self):
        return self._dotsPosition

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
                self.getNode(int((current.getCoordinates()[0] + neighbor.getCoordinates()[0])/2), int((current.getCoordinates()[1] + neighbor.getCoordinates()[1])/2)).changeState(2)
                self.generateMaze(neighbor)
    
    def spawnDots(self):
        positions = random.sample(self._freePositions, self.numberOfDots)
        for i, j in positions:
            self.getNode(i, j).changeState(3)


            


# def generate_maze(grid, current_node):
#     # Mark the current node as visited
#     grid[current_node] = "passage"

#     # Get a list of neighboring nodes
#     neighbors = get_neighbors(current_node)

#     # Randomly shuffle the list of neighbors
#     random.shuffle(neighbors)

#     # Iterate over the neighbors
#     for neighbor in neighbors:
#         if grid[neighbor] == "wall":
#             # Carve a passage to the neighbor
#             remove_wall(current_node, neighbor)
#             # Recursively call generate_maze with the neighbor as the current node
#             generate_maze(grid, neighbor)

# def get_neighbors(node):
#     # Returns a list of neighboring nodes
#     pass

# def remove_wall(node1, node2):
#     # Removes the wall between node1 and node2
#     pass

# # Example usage
# grid = initialize_grid()
# starting_node = choose_starting_node()
# generate_maze(grid, starting_node)




