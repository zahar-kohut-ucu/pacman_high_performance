import maze
import creatures
import movingAlgorithms
import time
import sys

sys.setrecursionlimit(100000)

a = time.time()

def simulate(m, n, ghostsAmount, cherries, numOfBroken, winTest = True, timeTest = False):
    myMaze = maze.Maze(m, n, ghostsAmount, cherries, numberOfBroken = numOfBroken, setSeed = True, seed = 2)
    
    pacmans = creatures.createPacmans()
    ghosts = creatures.createGhosts(ghostsAmount)

    myMaze.spawnPacmans(pacmans)
    myMaze.spawnGhosts(ghosts)
    
    GAME = True
    GHOST_MOVE_SWITCH = 1
    print("Game has started!")
    while GAME:
        print('move')
        newPacmanPositions = []
        newGhostsPosition = []

        for pacman in pacmans:
            newPacmanPositions.append(movingAlgorithms.getNextPacmanMove(myMaze, pacman))
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
                print("Dot found!")
            if move == 0 or pacman.getPoints() == myMaze.numberOfDots:
                GAME = False

        if GHOST_MOVE_SWITCH:
            GHOST_MOVE_SWITCH = 0
        else:
            GHOST_MOVE_SWITCH = 1

    if timeTest:
        return []
    elif winTest:
        return (pacmans[0].getPoints(), pacmans[1].getPoints()) 

print(simulate(200, 200, 20, 30, 4000))