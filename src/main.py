# Imports
import maze
import visualization
import pygame
import creatures

m = 21 # Number of rcolumns
n = 21 # Number of rows
k = 4  # Number of ghosts and dots

def main():
    
    myMaze = maze.Maze(m, n, k, setSeed = True, seed = 10)
    tileSize = 20
    width = myMaze.trueN
    height = myMaze.trueM

    screen = pygame.display.set_mode((width * tileSize, height * tileSize))
    pygame.display.set_caption("Pacman")

    pacmans =  creatures.createPacmans()
    ghosts =  creatures.createGhosts(k)

    visualization.initBoard(myMaze, screen, width, height)

    myMaze.spawnPacmans(pacmans)
    myMaze.spawnGhosts(ghosts)

    visualization.spawnCreatures(screen, ghosts, pacmans)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.flip()


if __name__ == '__main__':
    main()


