import numpy as np
import maze
import creatures
import movingAlgorithms
import time
import sys
from multiprocessing import Pool


sys.setrecursionlimit(100000)


a = time.time()

def simulate(m, n, ghostsAmount, cherries, numOfBroken, winTest = True, timeTest = False):
    THRDS = 4
    myPool = Pool(processes=THRDS)
    
    myMaze = maze.Maze(m, n, ghostsAmount, cherries, numberOfBroken = numOfBroken, setSeed = True, seed = 2)
    pacmans = creatures.createPacmans()
    ghosts = creatures.createGhosts(ghostsAmount)

    myMaze.spawnPacmans(pacmans)
    myMaze.spawnGhosts(ghosts)

    GAME = True
    GHOST_MOVE_SWITCH = 1
    while GAME:
        newPacmanPositions = []
        newGhostsPosition = []

        for pacman in pacmans:
            newPacmanPositions.append(movingAlgorithms.getNextPacmanMove(myMaze, pacman))
        if GHOST_MOVE_SWITCH:
            for ghost in ghosts:
                newPos = movingAlgorithms.getGhostNextMove(myMaze.maze, ghost, pacmans)
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

    if timeTest:
        return []
    elif winTest:
        return (pacmans[0].getPoints(), pacmans[1].getPoints()) 

print(simulate(200, 200, 4, 30, 4000))