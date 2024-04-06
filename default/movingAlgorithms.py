# Moving algorithm
# Imports
import heapq
import creatures
import maze
import random
import time

# Estimate euristic cost
def estimateEuristicCost(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

def isValid(myMaze, i, j, team = 0):
    if not team:
        return 0 <= i < myMaze.trueM and 0 <= j < myMaze.trueN and str(myMaze.getNode(i, j).getState()) != "wall"
    elif team == 1:
        return 0 <= i < myMaze.trueM and 0 <= j < myMaze.trueN//2 and str(myMaze.getNode(i, j).getState()) != "wall"
    else:
        return 0 <= i < myMaze.trueM and myMaze.trueN//2 < j < myMaze.trueN and str(myMaze.getNode(i, j).getState()) != "wall"

# Return random valid move
def allValidMoves(myMaze, position, team = 0):
    allMoves = [(position[0] - 1, position[1]), (position[0] + 1, position[1]), (position[0], position[1] - 1), (position[0], position[1] + 1)]
    possMoves = []
    for i, j in allMoves:
        if isValid(myMaze, i, j, team):
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
    a = time.time()
    visited = set()
    ways = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    pacmanPos = pacman.getCoordinates()
    distances = {pacmanPos: 0}
    queue = [(0 , pacmanPos)]
    ghostsPosition = myMaze.getGhostPositions(3 - pacman.getTeam())
    avoidPositions = []
    for i, j in ghostsPosition:
        if ((pacmanPos[1] == j and abs(pacmanPos[0] - i) < 5) or (pacmanPos[0] == i and abs(pacmanPos[1] - j) < 5) or (estimateEuristicCost(pacmanPos, (i,j)) < 7)):
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
        b = time.time()
        print("Time for one way:", b - a)
        return way[::-1]
    
    closestDist = float("inf")
    closestGhost = None
    for ghost in ghostsPosition:
        dist = estimateEuristicCost(pacmanPos, ghost)
        if dist < closestDist:
            closestGhost = ghost
            closestDist = dist
    b = time.time()
    print("Time for one way:", b - a)
    return [escapeGhost(myMaze, pacmanPos, closestGhost)]

#AStar
def aStarFindShortestPathTo(myMaze: maze.Maze, pacman, dotPos):
    a = time.time()
    visited = set()
    ways = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    pacmanPos = pacman.getCoordinates()
    distances = {pacmanPos: [0, estimateEuristicCost(pacmanPos, dotPos)]}
    queue = [(estimateEuristicCost(pacmanPos, dotPos), 0, pacmanPos)]
    ghostsPosition = myMaze.getGhostPositions(3 - pacman.getTeam())
    avoidPositions = []
    for i, j in ghostsPosition:
        if (pacmanPos[1] == j and abs(pacmanPos[0] - i) < 5) or (pacmanPos[0] == i and abs(pacmanPos[1] - j) < 5) or (estimateEuristicCost(pacmanPos, (i,j)) < 7):
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
            if 0 <= i < myMaze.trueM and 0 <= j < myMaze.trueN and str(myMaze.getNode(i, j).getState()) != "wall" and (i,j) not in avoidPositions:
                neighbour = (i, j)
                newDistance = distance + 1
                priority = newDistance + estimateEuristicCost(neighbour, dotPos)
                if neighbour not in distances:
                    distances[neighbour] = [0, 0]
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
        b = time.time()
        print("Time for one way:", b - a)
        return way[::-1]
    
    closestDist = float("inf")
    closestGhost = None
    for ghost in ghostsPosition:
        dist = estimateEuristicCost(pacmanPos, ghost)
        if dist < closestDist:
            closestGhost = ghost
            closestDist = dist
    b = time.time()
    print("Time for one way:", b - a)
    return [escapeGhost(myMaze, pacmanPos, closestGhost)]

# Returns new Pacman position

def getNextPacmanMove(myMaze: maze.Maze, pacman: creatures.Pacman, algo: int = 0):
    if not algo:
        algo = pacman.getTeam()
    algos = [dijkstraFindShortestPathTo, aStarFindShortestPathTo]
    dots = list(filter(lambda dot: myMaze.getNode(*dot).getTeam() != pacman.getTeam(), myMaze.getDotsPosition()))
    a = time.time()
    closest = min(dots, key= lambda dot: len(algos[algo - 1](myMaze, pacman, dot)))
    way = algos[algo - 1](myMaze, pacman, closest)
    b = time.time()
    print(b - a)
    try:
        nextMove = way[0]
    except IndexError:
        time.sleep(20)
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
        chaseMove = (ghost._x, ghost._y - 1 + 2 * (ghost._y < enemyPacman._y))
        if isValid(myMaze, *chaseMove, ghost.getTeam()):
            return chaseMove
    if verFound:
        chaseMove = (ghost._x - 1 + 2 * (ghost._x < enemyPacman._x), ghost._y)
        if isValid(myMaze, *chaseMove, ghost.getTeam()):
            return chaseMove 
    
    last_move = ghost.getLastMove()
    valid  = allValidMoves(myMaze, ghost.getCoordinates(), ghost.getTeam())
    validNorm = [(i - ghost._x, j - ghost._y) for i, j in valid]
    unwntdMove = (last_move[0]*-1, last_move[1]*-1)
    if unwntdMove in validNorm and len(valid) > 1:
        trashhold = min(ghost.cntInRow, 88)/(88*len(validNorm))
        proc = random.random()
        if proc < trashhold:
            return (ghost._x + unwntdMove[0], ghost._y + unwntdMove[1])
        validNorm.remove(unwntdMove)
        valid = [(ghost._x + i, ghost._y + j) for i, j in validNorm]
    return random.choice(valid)





