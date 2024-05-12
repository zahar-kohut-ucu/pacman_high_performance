# Moving algorithm
# Imports
import heapq
import random
import time
import numba
import numpy as np
# Estimate euristic cost
@numba.jit
def estimateEuristicCost(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

def isValid(mymaze, i, j, team = 0):
    if not team:
        return 0 <= i < mymaze.shape[0] and 0 <= j < mymaze.shape[1] and mymaze[i][j] != 1
    elif team == 1:
        return 0 <= i < mymaze.shape[0] and 0 <= j < mymaze.shape[1]//2 and mymaze[i][j] != 1
    else:
        return 0 <= i < mymaze.shape[0] and mymaze.shape[1]//2 < j < mymaze.shape[1] and mymaze[i][j] != 1

# Return random valid move
def allValidMoves(mymaze, position, team = 0):
    allMoves = [(position[0] - 1, position[1]), (position[0] + 1, position[1]), (position[0], position[1] - 1), (position[0], position[1] + 1)]
    possMoves = []
    for i, j in allMoves:
        if isValid(mymaze, i, j, team):
            possMoves.append((i, j))
    return possMoves

# Escaping ghost logic
def escapeGhost(mymaze, pacmanPos, ghostPos):
    hor = (pacmanPos[0], pacmanPos[1] - 1 + 2 * (pacmanPos[1] > ghostPos[1]))
    ver = (pacmanPos[0] - 1 + 2 * (pacmanPos[0] > ghostPos[0]), pacmanPos[1])
    if pacmanPos[0] == ghostPos[0] and isValid(mymaze, hor[0], hor[1]):
        return hor
    elif pacmanPos[1] == ghostPos[1] and isValid(mymaze, ver[0], ver[1]):
        return ver
    else:
        validMoves = allValidMoves(mymaze, pacmanPos)
        maxDistance = -1
        bestMove = None
        for move in validMoves:
            distance = estimateEuristicCost(ghostPos, move)
            if distance > maxDistance:
                maxDistance = distance
                bestMove = move
        return bestMove

# Dijkstra
@numba.jit
def dijkstraFindShortestPathTo(mymaze, ghostsPosition, pacman, dotPos):
    visited = set()
    ways = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    pacmanPos = (pacman[0], pacman[1])
    distances = {pacmanPos: 0}
    queue = [(0 , pacmanPos)]
    avoidPositions = []
    for i, j in ghostsPosition:
        if ((pacman[1] == j and abs(pacman[0] - i) < 5) or (pacman[0] == i and abs(pacman[1] - j) < 5) or (estimateEuristicCost(pacmanPos, (i,j)) < 7)):
            avoidPositions.append((i, j))
            for di in range(-1, 2):
                for dj in range(-1, 2):
                    avoidPositions.append((i+di, j+dj))
    while queue:
        distance, curr = heapq.heappop(queue)

        if curr == dotPos:
            break

        if curr in visited:
            continue

        visited.add(curr)

        for di, dj in ways:
            i, j = curr[0] + di, curr[1] + dj
            if  0 <= i < mymaze.shape[0] and 0 <= j < mymaze.shape[1] and mymaze[i][j] != 1 and (i,j) not in avoidPositions:
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

#AStar
@numba.jit
def aStarFindShortestPathTo(mymaze, ghostsPosition, pacman, dotPos):
    visited = set()
    ways = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    pacmanPos = (pacman[0], pacman[1])
    initCost = estimateEuristicCost(pacmanPos, dotPos)
    distances = {pacmanPos: np.array([0, initCost])}
    queue = [(estimateEuristicCost(pacmanPos, dotPos), 0, pacmanPos)]
    avoidPositions = []
    for i, j in ghostsPosition:
        if (pacman[1] == j and abs(pacman[0] - i) < 5) or (pacman[0] == i and abs(pacman[1] - j) < 5) or (estimateEuristicCost(pacmanPos, (i,j)) < 7):
            avoidPositions.append((i, j))
            for di in range(-1, 2):
                for dj in range(-1, 2):
                    avoidPositions.append((i+di, j+dj))

    while queue:
        _, distance, curr = heapq.heappop(queue)

        if curr == dotPos:
            break

        if curr in visited:
            continue

        visited.add(curr)

        for di, dj in ways:
            i, j = curr[0] + di, curr[1] + dj
            if  0 <= i < mymaze.shape[0] and 0 <= j < mymaze.shape[1] and mymaze[i][j] != 1 and (i,j) not in avoidPositions:
                neighbour = (i, j)
                newDistance = distance + 1
                priority = newDistance + estimateEuristicCost(neighbour, dotPos)
                if neighbour not in distances:
                    distances[neighbour] = np.array([0, 0])
                    distances[neighbour][0] = newDistance
                    distances[neighbour][1] = priority
                    heapq.heappush(queue, (priority, newDistance, neighbour))
                elif priority < distances[neighbour][1]:
                    distances[neighbour][0] = newDistance
                    distances[neighbour][1] = priority
                    heapq.heappush(queue, (priority, newDistance, neighbour))

    way = []
    curr = dotPos
    if curr in distances:
        while curr != pacmanPos:
            way.append(curr)
            for di, dj in ways:
                i, j = curr[0] - di, curr[1] - dj
                if (i, j) in distances and distances[curr][0] == distances[(i, j)][0] + 1:
                    curr = (i, j)
                    break
        return way[::-1]
    


# Returns new Pacman position
def getNextPacmanMove(mypool, myMaze, pacman, algo: int = 0):
    if not algo:
        algo = pacman[2]
    algos = [dijkstraFindShortestPathTo, aStarFindShortestPathTo]
    dots = myMaze.yellowDotsPosition if algo == 1 else myMaze.redDotsPosition
    ghostsPos = myMaze.ghostsPosition1 if pacman[2] == 2 else myMaze.ghostsPosition2

    items = [(myMaze.maze, ghostsPos, pacman, dot) for dot in dots]
    shortest = float("inf")
    chosenWay = None

    a = time.time()
    res = mypool.starmap_async(algos[algo - 1], items)
    ways = res.get()
    for way in ways:
        if way and len(way) < shortest:
            chosenWay = way
    if not chosenWay:
        closestDist = float("inf")
        closestGhost = None
        for ghost in ghostsPos:
            dist = estimateEuristicCost((pacman[0], pacman[1]), ghost)
            if dist < closestDist:
                closestGhost = ghost
                closestDist = dist
        chosenWay = [escapeGhost(myMaze.maze, (pacman[0], pacman[1]), closestGhost)]
    b = time.time()
    if algo == 1:
        print("Dijksta's:", b - a)
    else:
        print("A-star:", b - a)    
    nextMove = chosenWay[0]
    return nextMove

# Returns new ghost position
def getGhostNextMove(mymaze, ghost, pacmans):
    # look for Pacman
    enemyPacman = pacmans[0] if pacmans[0][2] != ghost[2] else pacmans[1]
    horFound = True if ghost[0] == enemyPacman[0] else False
    for j in range(min(ghost[1], enemyPacman[1]) + 1, max(ghost[1], enemyPacman[1])):
        if horFound:
            if mymaze[ghost[0]][j] != 1:
                continue
            else:
                horFound = False
        else:
            break

    verFound = True if ghost[1] == enemyPacman[1] and not horFound else False
    for i in range(min(ghost[0], enemyPacman[0]) + 1, max(ghost[0], enemyPacman[0])):
        if verFound:
            if mymaze[i][ghost[1]] != 1:
                continue
            else:
                verFound = False
        else:
            break
    # choose move
    if horFound:
        chaseMove = (ghost[0], ghost[1] - 1 + 2 * (ghost[1] < enemyPacman[1]))
        if isValid(mymaze, *chaseMove, ghost[2]):
            return chaseMove
    if verFound:
        chaseMove = (ghost[0] - 1 + 2 * (ghost[0] < enemyPacman[0]), ghost[1])
        if isValid(mymaze, *chaseMove, ghost[2]):
            return chaseMove 
    
    last_move = (ghost[4], ghost[5])
    valid  = allValidMoves(mymaze, (ghost[0], ghost[1]), ghost[2])
    validNorm = [(i - ghost[0], j - ghost[1]) for i, j in valid]
    unwntdMove = (last_move[0]*-1, last_move[1]*-1)
    if unwntdMove in validNorm and len(valid) > 1:
        trashhold = min(ghost[3], 88)/(88*len(validNorm))
        proc = random.random()
        if proc < trashhold:
            return (ghost[0] + unwntdMove[0], ghost[1] + unwntdMove[1])
        validNorm.remove(unwntdMove)
        valid = [(ghost[0] + i, ghost[1] + j) for i, j in validNorm]
    return random.choice(valid)





