import maze
import creatures
import movingAlgorithms
import time
import sys
from multiprocessing import Pool


sys.setrecursionlimit(100000)

def simulate(m, n, ghostsAmount, cherries, numOfBroken, sed):
    THRDS = 4
    myMaze = maze.Maze(m, n, ghostsAmount, cherries, numberOfBroken = numOfBroken, setSeed = True, seed = sed)
    
    pacmans = creatures.createPacmans()
    ghosts = creatures.createGhosts(ghostsAmount)
    
    myPool = Pool(processes=THRDS)

    myMaze.spawnPacmans(pacmans)
    myMaze.spawnGhosts(ghosts)
    
    GAME = True
    GHOST_MOVE_SWITCH = 1
    a = time.time()
    while GAME:
        newPacmanPositions = []
        newGhostsPosition = []

        for pacman in pacmans:
            newPacmanPositions.append(movingAlgorithms.getNextPacmanMove(myPool, myMaze, pacman, THRDS))
        if GHOST_MOVE_SWITCH:
            for ghost in ghosts:
                newPos = movingAlgorithms.getGhostNextMove(myMaze, ghost, pacmans)
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

    myPool.close()
    b = time.time()
    return (pacmans[0].getPoints(), pacmans[1].getPoints(), b - a) 

print(simulate(25, 25, 4, 70, 50, 2))