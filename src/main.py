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

    screen = pygame.display.set_mode(((width + 2) * tileSize, (height + 2) * tileSize))
    pygame.display.set_caption("Pacman")

    pacmans =  creatures.createPacmans()
    ghosts =  creatures.createGhosts(k)

    visualization.initBoard(myMaze, screen, width, height)
    visualization.drawBorders(screen, width, height)

    myMaze.spawnPacmans(pacmans)
    myMaze.spawnGhosts(ghosts)

    visualization.spawnCreatures(screen, ghosts, pacmans)
    pygame.display.flip()

    oldPacmans = [p.getCoordinates() for p in pacmans]
    oldGhosts = [g.getCoordinates() for g in ghosts]
    myMaze.changeCreaturesCoordinates(pacmans, ghosts, [[0,1], [0,2]], [[0,4], [0,5], [0,6], [0,7], [0,8], [0,9], [0,10], [0,12]])
    visualization.redrawBoard(screen, myMaze, pacmans, ghosts, oldGhosts + oldPacmans)
    pygame.display.flip()



    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        pygame.display.flip()
        



if __name__ == '__main__':
    main()


