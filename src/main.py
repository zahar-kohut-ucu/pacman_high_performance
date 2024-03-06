# Imports
import maze
import visualization
import pygame
import creatures
import movingAlgorithms
import time

m = 50 # Number of columns
n = 50 # Number of rows
k = 4  # Number of ghosts and dots

def main():
    myMaze = maze.Maze(m, n, k, setSeed = True, seed = 13)
    tileSize = 20
    width = myMaze.trueN
    height = myMaze.trueM

    pygame.font.init()
    font = pygame.font.SysFont('freesansbold.ttf', 24)

    screen = pygame.display.set_mode(((width + 2) * tileSize, (height + 5) * tileSize))
    pygame.display.set_caption("Pacman")

    pacmans =  creatures.createPacmans()
    ghosts =  creatures.createGhosts(k)

    visualization.initBoard(myMaze, screen, width, height)
    visualization.drawBorders(screen, width, height)

    myMaze.spawnPacmans(pacmans)
    myMaze.spawnGhosts(ghosts)

    visualization.spawnCreatures(screen, ghosts, pacmans)
    pygame.display.flip()

    GAME = True
    DELAY = 0.05
    GHOST_MOVE_SWITCH = 1

    while GAME:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        time.sleep(DELAY)
        oldPacmans = [p.getCoordinates() for p in pacmans]
        if GHOST_MOVE_SWITCH:
            oldGhosts = [g.getCoordinates() for g in ghosts]
        else:
            oldGhosts = []
        newPacmanPositions = []
        newGhostsPosition = []

        for pacman in pacmans:
            newPacmanPositions.append(movingAlgorithms.getNextPacmanMove(myMaze, pacman))
        for ghost in ghosts:
            newGhostsPosition.append(movingAlgorithms.getGhostNextMove(myMaze, ghost, pacmans))

        myMaze.changePacmansCoordinates(pacmans, newPacmanPositions)
        for pacman in pacmans:
            move = myMaze.checkMove(pacman)
            if move == 0:
                GAME = False
        if GHOST_MOVE_SWITCH:
            myMaze.changeGhostsCoordinates(ghosts, newGhostsPosition)

        visualization.redrawBoard(screen, myMaze, pacmans, ghosts, oldGhosts + oldPacmans)
        for pacman in pacmans:
            move = myMaze.checkMove(pacman)
            if move == 0:
                GAME = False
            elif move == 1:
                myMaze.eatAndRespawnDot(pacman)

        if GHOST_MOVE_SWITCH:
            GHOST_MOVE_SWITCH = 0
        else:
            GHOST_MOVE_SWITCH = 1
        text = font.render("Pac 1: " + str(pacmans[0].getPoints()) + " Pac 2: " + str(pacmans[1].getPoints()), True, (0, 255, 0))
        refresher = pygame.Rect(0, (height + 3) * tileSize, tileSize * width, tileSize * 2)
        pygame.draw.rect(screen, (0, 0, 0), refresher)
        screen.blit(text, ((width-4) * tileSize // 2, (height + 3) * tileSize))
        pygame.display.flip()

    print(f"Yellow : {pacmans[0].getPoints()} Red : {pacmans[1].getPoints()}")
    time.sleep(3)
    pygame.quit()


if __name__ == '__main__':
    main()


