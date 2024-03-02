# Visualization of playing board
# Imports
import pygame
import nodeStates
import maze


def initBoard(maze: maze.Maze, screen: pygame.Surface, width: int, height: int, tileSize: int = 20):
    screen.fill((255, 255, 255))
    for x in range(height):
        for y in range(width):
            team = maze.getNode(x, y).getTeam()
            if  team < 1:
                team = ''
            
            iconImage = pygame.image.load(f"src/icons/{str(maze.getNode(x, y).getState())}{team}.png")
            screen.blit(iconImage, (y*tileSize, x*tileSize))


def spawnCreatures(screen: pygame.Surface, ghosts: list, pacmans: list, tileSize: int = 20):
    for ghost in ghosts:
        x, y = ghost.getCoordinates()
        iconImage = pygame.image.load(f"src/icons/ghost{ghost.getTeam()}.png")
        screen.blit(iconImage, (y*tileSize, x*tileSize))
    
    for pacman in pacmans:
        x, y = pacman.getCoordinates()
        iconImage = pygame.image.load(f"src/icons/pacman{pacman.getTeam()}.png")
        screen.blit(iconImage, (y*tileSize, x*tileSize))