# Visualization of playing board
# Imports
import pygame
import nodeStates
import maze


def initBoard(maze: maze.Maze, screen: pygame.Surface, width: int, height: int, tileSize: int = 20):
    screen.fill((255, 255, 255))
    for i in range(height):
        for j in range(width):
            iconImage = pygame.image.load(f"src/icons/{str(maze.getNode(i, j).getState())}.png")
            screen.blit(iconImage, (j*tileSize, i*tileSize))
