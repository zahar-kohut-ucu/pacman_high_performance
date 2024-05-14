import maze1 as maze1
import creatures1 as creatures1
import movingAlgorithms1 as movingAlgorithms1
import time
import sys

sys.setrecursionlimit(100000)

def simulate(m, n, ghostsAmount, cherries, numOfBroken, sed):
    myMaze = maze1.Maze(m, n, ghostsAmount, cherries, numberOfBroken = numOfBroken, setSeed = True, seed = sed)
    
    pacmans = creatures1.createPacmans()
    ghosts = creatures1.createGhosts(ghostsAmount)

    myMaze.spawnPacmans(pacmans)
    myMaze.spawnGhosts(ghosts)
    
    GAME = True
    GHOST_MOVE_SWITCH = 1
    a  = time.time()
    while GAME:
        newPacmanPositions = []
        newGhostsPosition = []

        for pacman in pacmans:
            newPacmanPositions.append(movingAlgorithms1.getNextPacmanMove(myMaze, pacman))
        if GHOST_MOVE_SWITCH:
            for ghost in ghosts:
                newPos = movingAlgorithms1.getGhostNextMove(myMaze, ghost, pacmans)
                newGhostsPosition.append(newPos)
                ghost.setLastMove((newPos[0] - ghost._x, newPos[1] - ghost._y))

        myMaze.changePacmansCoordinates(pacmans, newPacmanPositions)
        for pacman in pacmans:
            move = myMaze.checkMove(pacman)
            if move == 0:
                GAME = False
        if GHOST_MOVE_SWITCH:
            myMaze.changeGhostsCoordinates(ghosts, newGhostsPosition)

        for pacman in pacmans:
            move = myMaze.checkMove(pacman)
            # if move == 0:
            #     GAME = False
            if move == 1:
                myMaze.eatAndRespawnDot(pacman)
            if move == 0 or pacman.getPoints() == myMaze.numberOfDots:
                GAME = False

        if GHOST_MOVE_SWITCH:
            GHOST_MOVE_SWITCH = 0
        else:
            GHOST_MOVE_SWITCH = 1
    b = time.time()
    return [pacmans[0].getPoints(), pacmans[1].getPoints(), b - a]

# print(simulate(25, 25, 4, 70, 50, 2))