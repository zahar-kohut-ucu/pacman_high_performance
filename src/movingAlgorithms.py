# Moving algorithm
# Imports
import heapq
import creatures
import maze
import random

# Estimate euristic cost
def estimateEuristicCost(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

def isValid(myMaze, i, j):
    return 0 <= i < myMaze.trueM and 0 <= j < myMaze.trueN and str(myMaze.getNode(i, j).getState()) != "wall"

# Return random valid move
def allValidMoves(myMaze, position):
    allMoves = [(position[0] - 1, position[1]), (position[0] + 1, position[1]), (position[0], position[1] - 1), (position[0], position[1] + 1)]
    possMoves = []
    for i, j in allMoves:
        if isValid(myMaze, i, j):
            possMoves.append((i, j))
    return possMoves

# Escaping ghost logic
def escapeGhost(myMaze, pacmanPos, ghostPos):
    hor = (pacmanPos[0], pacmanPos[1] - 1 + 2 * (pacmanPos[1] > ghostPos[1]))
    ver = (pacmanPos[0] - 1 + 2 * (pacmanPos[0] > ghostPos[0]), pacmanPos[1])
    if pacmanPos[0] == ghostPos[0] and isValid(myMaze, hor[0], hor[1]):
        return hor
    elif pacmanPos[1] == ghostPos[1] and isValid(myMaze, ver[0], ver[1]):
        return ver
    else:
        validMoves = allValidMoves(myMaze, pacmanPos)
        maxDistance = -1
        bestMove = None
        for move in validMoves:
            distance = estimateEuristicCost(ghostPos, move)
            if distance > maxDistance:
                maxDistance = distance
                bestMove = move
        return bestMove


# Dijkstra
def dijkstraFindShortestPathTo(myMaze: maze.Maze, pacman, dotPos):
    visited = set()
    ways = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    pacmanPos = pacman.getCoordinates()
    distances = {pacmanPos: 0}
    queue = [(0 , pacmanPos)]
    avoidPositions = []
    for i, j in myMaze.getGhostPositions(3 - pacman.getTeam()):
        if ((pacmanPos[1] == j and abs(pacmanPos[0] - i) < 4) or (pacmanPos[0] == i and abs(pacmanPos[1] - j) < 4) or (pacmanPos[0] == i and pacmanPos[1] == j and estimateEuristicCost(pacmanPos, (i,j)) < 7)) and (i, j) != dotPos:
            avoidPositions.append((i, j))
    while queue:
        distance, curr = heapq.heappop(queue)

        if curr == dotPos:
            break

        if curr in visited:
            continue

        visited.add(curr)

        for di, dj in ways:
            i, j = curr[0] + di, curr[1] + dj
            if 0 <= i < myMaze.trueM and 0 <= j < myMaze.trueN and str(myMaze.getNode(i, j).getState()) != "wall" and (i,j) not in avoidPositions:
                neighbour = (i, j)
                newDistance = distance + 1
                if neighbour not in distances or newDistance < distances[neighbour]:
                    distances[neighbour] = newDistance
                    heapq.heappush(queue, (newDistance, neighbour))

    way = []
    curr = dotPos
    if curr in distances:
        while curr != pacmanPos:
            way.append(curr)
            for di, dj in ways:
                i, j = curr[0] - di, curr[1] - dj
                if (i, j) in distances and distances[curr] == distances[(i, j)] + 1:
                    curr = (i, j)
                    break
        return way[::-1]
    return [escapeGhost(myMaze, pacmanPos, avoidPositions[0])]


def aStarFindShortestPathTo(myMaze: maze.Maze, pacman, dotPos):
    visited = set()
    ways = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    pacmanPos = pacman.getCoordinates()
    distances = {pacmanPos: 0}
    queue = [(0 , pacmanPos)]
    avoidPositions = []
    for i, j in myMaze.getGhostPositions(3 - pacman.getTeam()):
        if (pacmanPos[1] == j and abs(pacmanPos[0] - i) < 3) or (pacmanPos[0] == i and abs(pacmanPos[1] - j) < 3) and (i, j) != dotPos:
            avoidPositions.append((i, j))

    while queue:
        distance, curr = heapq.heappop(queue)

        if curr == dotPos:
            break

        if curr in visited:
            continue

        visited.add(curr)

        for di, dj in ways:
            i, j = curr[0] + di, curr[1] + dj
            if 0 <= i < myMaze.trueM and 0 <= j < myMaze.trueN and str(myMaze.getNode(i, j).getState()) != "wall" and (i,j) not in avoidPositions:
                neighbour = (i, j)
                newDistance = distance + 1
                if neighbour not in distances or newDistance < distances[neighbour]:
                    distances[neighbour] = newDistance
                    priority = newDistance + estimateEuristicCost(neighbour, dotPos)
                    heapq.heappush(queue, (priority, neighbour))

    way = []
    curr = dotPos
    if curr in distances:
        while curr != pacmanPos:
            way.append(curr)
            minNeighbour = None
            minDist = float("inf")
            for di, dj in ways:
                i, j = curr[0] - di, curr[1] - dj
                if  (i, j) in distances and distances[curr] < minDist:
                    minDist = distances[i, j]
                    minNeighbour = (i, j)
            curr = minNeighbour
        return way[::-1]
    return [escapeGhost(myMaze, pacmanPos, avoidPositions[0])]

# Returns new Pacman position

def getNextPacmanMove(myMaze: maze.Maze, pacman: creatures.Pacman, algo: int = 0):
    if not algo:
        algo = pacman.getTeam()
    algos = [dijkstraFindShortestPathTo, aStarFindShortestPathTo]
    dots = list(filter(lambda dot: myMaze.getNode(*dot).getTeam() != pacman.getTeam(), myMaze.getDotsPosition()))
    closest = min(dots, key= lambda dot: len(algos[algo - 1](myMaze, pacman, dot)))
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
    return random.choice(allValidMoves(myMaze, ghost.getCoordinates()))





