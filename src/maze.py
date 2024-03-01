# Maze implementation
# Imports
import node
import random

class Maze:
    def __init__(self, m: int = 35, n: int = 35, numberOfDots: int = 4):
        self._maze = [[node.Node(i, j, node.nodeStates.wallState) for j in range(n)] for i in range(m)]
        self._freePositions = []
        self._dotsPosition = []

    def getDotsPosition(self):
        return self._dotsPosition

    def getNode(self, i: int, j: int):
        return self._maze[i][j]

    def getNeighbours(self, current):
        pass

    # maze generator using DFS
    def generateMaze(self, current):
        # getting neighbours
        pass

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




