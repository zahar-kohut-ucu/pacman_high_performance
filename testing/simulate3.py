import numpy as np
import maze3 as maze3
import creatures3 as creatures3
import movingAlgorithms3 as movingAlgorithms3
import time
import sys

sys.setrecursionlimit(100000)

def simulate(m, n, ghostsAmount, cherries, numOfBroken, sed, winTest = True, timeTest = False):
    myMaze = maze3.Maze(m, n, ghostsAmount, cherries, numberOfBroken = numOfBroken, setSeed = True, seed = sed)
    pacmans = creatures3.createPacmans()
    ghosts = creatures3.createGhosts(ghostsAmount)

    myMaze.spawnPacmans(pacmans)
    myMaze.spawnGhosts(ghosts)

    GAME = True
    GHOST_MOVE_SWITCH = 1
    a = time.time()
    while GAME:
        newPacmanPositions = []
        newGhostsPosition = []

        for pacman in pacmans:
            newPacmanPositions.append(movingAlgorithms3.getNextPacmanMove(myMaze, pacman))
        if GHOST_MOVE_SWITCH:
            for ghost in ghosts:
                newPos = movingAlgorithms3.getGhostNextMove(myMaze.maze, ghost, pacmans)
                newGhostsPosition.append(newPos)
                if (newPos[0] - ghost[0]) == ghost[4] and (newPos[1] - ghost[1]) == ghost[5]:
                    ghost[3] += 1
                else:
                    ghost[4], ghost[5] = newPos[0] - ghost[0], newPos[1] - ghost[1]
                    ghost[3] = 1

        myMaze.changePacmansCoordinates(pacmans, newPacmanPositions)
        for pacman in pacmans:
            move = myMaze.checkMove(pacman)
            if move == 0:
                GAME = False
        if GHOST_MOVE_SWITCH:
            myMaze.changeGhostsCoordinates(ghosts, newGhostsPosition)

        for pacman in pacmans:
            move = myMaze.checkMove(pacman)

            if move == 1:
                myMaze.eatAndRespawnDot(pacman)
            if move == 0 or pacman[4] == myMaze.numberOfDots:
                GAME = False

        if GHOST_MOVE_SWITCH:
            GHOST_MOVE_SWITCH = 0
        else:
            GHOST_MOVE_SWITCH = 1
    b = time.time()
    return [pacmans[0][-1], pacmans[1][-1], b - a]

# print(simulate(25, 25, 4, 70, 50, 2))