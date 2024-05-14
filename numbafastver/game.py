import numpy as np
import maze
import creatures
import visualization
import movingAlgorithms
import pygame
import time
import sys

sys.setrecursionlimit(100000)

m = 25 # Number of columns
n = 25 # Number of rows

cherries = 70  # Number of ghosts and dots
ghostsAmount = 4
numOfBroken = 50

def main():
    myMaze = maze.Maze(m, n, ghostsAmount, cherries, numberOfBroken = numOfBroken, setSeed = True, seed = 3)
    tileSize = 20
    width = myMaze.trueN
    height = myMaze.trueM

    pygame.font.init()
    font = pygame.font.SysFont('freesansbold.ttf', 24)

    screen = pygame.display.set_mode(((width + 2) * tileSize, (height + 5) * tileSize))
    pygame.display.set_caption("Pacman")

    pacmans = creatures.createPacmans()
    ghosts = creatures.createGhosts(ghostsAmount)

    # print(myMaze.maze)
    # time.sleep(180)
    visualization.initBoard(myMaze, screen, width, height, tileSize=tileSize)
    visualization.drawBorders(screen, width, height, tileSize=tileSize)

    myMaze.spawnPacmans(pacmans)
    myMaze.spawnGhosts(ghosts)

    visualization.spawnCreatures(screen, ghosts, pacmans, tileSize=tileSize)
    pygame.display.flip()

    GAME = True
    DELAY = 0.05
    GHOST_MOVE_SWITCH = 1
    print("g")
    while GAME:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        time.sleep(DELAY)
        oldPacmans = [(p[0], p[1]) for p in pacmans]
        if GHOST_MOVE_SWITCH:
            oldGhosts = [[g[0], g[1]] for g in ghosts]
        else:
            oldGhosts = []

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

        visualization.redrawBoard(screen, myMaze, pacmans, ghosts, oldGhosts + oldPacmans, tileSize=tileSize)
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

        text = font.render("Pac 1: " + str(pacmans[0][4]) + " Pac 2: " + str(pacmans[1][4]), True, (0, 255, 0))
        refresher = pygame.Rect(0, (height + 3) * tileSize, tileSize * width, tileSize * 2)
        pygame.draw.rect(screen, (0, 0, 0), refresher)
        screen.blit(text, ((width-4) * tileSize // 2, (height + 3) * tileSize))
        pygame.display.flip()

    print(f"Yellow : {pacmans[0][4]} Red : {pacmans[1][4]}")
    time.sleep(5)
    pygame.quit()

if __name__ == "__main__":
    main()