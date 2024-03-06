# Moving algorithm
# Imports 
import heapq
import creatures
import maze
import random

# Dijkstra
def dijkstraFindShortestPathTo(myMaze: maze.Maze, pacman, dotPos):
    visited = set()
    ways = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    distances = {pacman.getCoordinates(): 0}
    queue = [(0 , pacman.getCoordinates())]

    while queue:
        distance, curr = heapq.heappop(queue)

        if curr == dotPos:
            break
        
        if curr in visited:
            continue

        visited.add(curr)

        for di, dj in ways:
            i, j = curr[0] + di, curr[1] + dj
            if 0 <= i < myMaze.trueM and 0 <= j < myMaze.trueN and str(myMaze.getNode(i, j).getState()) != "wall":# and (i,j) not in myMaze.getGhostPositions(3 - pacman.getTeam()):
                neighbour = (i, j)
                newDistance = distance + 1
                if neighbour not in distances or newDistance < distances[neighbour]:
                    distances[neighbour] = newDistance
                    heapq.heappush(queue, (newDistance, neighbour))

    way = []
    curr = dotPos
    while curr != pacman.getCoordinates():
        way.append(curr)
        for di, dj in ways:
            i, j = curr[0] - di, curr[1] - dj
            if (i, j) in distances and distances[curr] == distances[(i, j)] + 1:
                curr = (i, j)
                break
    return way[::-1]

def estimateEuristicCost(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

def aStarFindShortestPathTo(myMaze: maze.Maze, pacman, dotPos):
    visited = set()
    ways = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    distances = {pacman.getCoordinates(): 0}
    queue = [(0 , pacman.getCoordinates())]

    while queue:
        distance, curr = heapq.heappop(queue)

        if curr == dotPos:
            break
        
        if curr in visited:
            continue

        visited.add(curr)

        for di, dj in ways:
            i, j = curr[0] + di, curr[1] + dj
            if 0 <= i < myMaze.trueM and 0 <= j < myMaze.trueN and str(myMaze.getNode(i, j).getState()) != "wall":# and (i,j) not in myMaze.getGhostPositions(3 - pacman.getTeam()):
                neighbour = (i, j)
                newDistance = distance + 1
                if neighbour not in distances or newDistance < distances[neighbour]:
                    distances[neighbour] = newDistance
                    priority = newDistance + estimateEuristicCost(neighbour, dotPos)
                    heapq.heappush(queue, (priority, neighbour))

    way = []
    curr = dotPos
    while curr != pacman.getCoordinates():
        way.append(curr)
        minNeighbour = None
        minDist = float("inf")
        for di, dj in ways:
            i, j = curr[0] - di, curr[1] - dj
            if (i, j) in distances and distances[curr] < minDist:
                minDist = distances[i, j]
                minNeighbour = (i, j)
        curr = minNeighbour
    return way[::-1]

# Returns new Pacman position

def getNextPacmanMove(myMaze: maze.Maze, pacman: creatures.Pacman, algo: int = 0):
    if not algo:
        algo = pacman.getTeam()
    algos = [dijkstraFindShortestPathTo, aStarFindShortestPathTo]
    dots = list(filter(lambda dot: myMaze.getNode(*dot).getTeam() != pacman.getTeam(), myMaze.getDotsPosition()))
    closest = min(dots, key= lambda dot: len(algos[algo - 1](myMaze, pacman, dot)))
    print(pacman.getCoordinates())
    print(closest)
    way = algos[algo - 1](myMaze, pacman, closest)
    nextMove = way[0]
    return nextMove

# Returns new ghost position
def getGhostNextMove(myMaze: maze.Maze, ghost: creatures.Ghost, pacmans):
    # look for Pacman
    enemyPacman = pacmans[0] if pacmans[0].getTeam() != ghost.getTeam() else pacmans[1]
    horFound = True if ghost._x == enemyPacman._x else False
    for j in range(min(ghost._y, enemyPacman._y) + 1, max(ghost._y, enemyPacman._y)):
        if horFound:
            if str(myMaze.getNode(ghost._x, j).getState()) != "wall":
                continue
            else:
                horFound = False
        else:
            break

    verFound = True if ghost._y == enemyPacman._y and not horFound else False
    for i in range(min(ghost._x, enemyPacman._x) + 1, max(ghost._x, enemyPacman._x)):
        if verFound:
            if str(myMaze.getNode(i, ghost._y).getState()) != "wall":
                continue
            else:
                verFound = False
        else:
            break
    # choose move
    if horFound:
        return (ghost._x, ghost._y - 1 + 2 * (ghost._y < enemyPacman._y))
    if verFound:
        return (ghost._x - 1 + 2 * (ghost._x < enemyPacman._x), ghost._y)

    allMoves = [(ghost._x - 1, ghost._y), (ghost._x + 1, ghost._y), (ghost._x, ghost._y - 1), (ghost._x, ghost._y + 1)]
    possMoves = []
    for i, j in allMoves:
        if 0 <= i < myMaze.trueM and 0 <= j < myMaze.trueN and str(myMaze.getNode(i, j).getState()) != "wall":
            possMoves.append((i, j))
    return random.choice(possMoves)


        
        
        
