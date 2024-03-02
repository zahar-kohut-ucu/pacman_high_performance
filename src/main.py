# Imports
import maze
import visualization
import pygame

m = 21
n = 21

def main():
    myMaze = maze.Maze(m, n, 5, setSeed = True, seed = 130)
    tileSize = 20
    width = myMaze.trueN
    height = myMaze.trueM

    screen = pygame.display.set_mode((width * tileSize, height * tileSize))
    pygame.display.set_caption("Pacman")

    visualization.initBoard(myMaze, screen, width, height)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.flip()


if __name__ == '__main__':
    main()


