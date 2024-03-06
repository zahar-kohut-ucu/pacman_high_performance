# Imports
import maze
import visualization
import pygame
import creatures
import movingAlgorithms
import time

m = 21 # Number of rcolumns
n = 21 # Number of rows
k = 4  # Number of ghosts and dots

def main():
    
    myMaze = maze.Maze(m, n, k, setSeed = True, seed = 132)
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

    while GAME:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
        time.sleep(0.2)
        oldPacmans = [p.getCoordinates() for p in pacmans]
        oldGhosts = [g.getCoordinates() for g in ghosts]
        newPacmanPositions = []
        newGhostsPosition = []

        for pacman in pacmans:
            newPacmanPositions.append(movingAlgorithms.getNextPacmanMove(myMaze, pacman, algo=1))
        for ghost in ghosts:    
            newGhostsPosition.append(movingAlgorithms.getGhostNextMove(myMaze, ghost, pacmans))
        
        myMaze.changeCreaturesCoordinates(pacmans, ghosts, newPacmanPositions, newGhostsPosition)
        visualization.redrawBoard(screen, myMaze, pacmans, ghosts, oldGhosts + oldPacmans)
        for pacman in pacmans:
            move = myMaze.checkMove(pacman)
            if move == 0:
                GAME = False
            elif move == 1:
                myMaze.eatAndRespawnDot(pacman)
                text_surface = font.render("Pac 1: " + str(pacmans[0].getPoints()) + " Pac 2: " + str(pacmans[1].getPoints()), True, (0, 255, 0))
                fill_rect = pygame.Rect(0, (height + 3) * tileSize, tileSize * width, tileSize * 2) 
                pygame.draw.rect(screen, (0, 0, 0), fill_rect)
                screen.blit(text_surface, ((width-4) * tileSize // 2, (height + 3) * tileSize))
        pygame.display.flip()

    time.sleep(5)
    pygame.quit()

        
if __name__ == '__main__':
    main()


