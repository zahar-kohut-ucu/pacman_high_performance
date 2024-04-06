# Visualization of playing board
# Imports
import pygame
import maze
import node


def drawTile(screen: pygame.Surface, tile: node.Node, tileSize: int = 20):
    team = tile.getTeam()
    x, y = tile.getCoordinates()
    if  team < 1:
        team = ''

    iconImage = pygame.image.load(f"default/icons/{str(tile.getState())}{team}.png")
    screen.blit(iconImage, ((y + 1) * tileSize, (x + 1) * tileSize))
    

def initBoard(maze: maze.Maze, screen: pygame.Surface, width: int, height: int, tileSize: int = 20):
    screen.fill((0, 0, 0))
    for x in range(height):
        for y in range(width):
            tile = maze.getNode(x, y)
            drawTile(screen, tile)

def drawBorders(screen: pygame.Surface, width: int, height: int, tileSize: int = 20):
    for x in range(height+2):
        iconImage = pygame.image.load(f"default/icons/wall.png")
        screen.blit(iconImage, (0, x * tileSize))
        screen.blit(iconImage, ((width + 1) * tileSize, x * tileSize))
    for y in range(width+2):
        iconImage = pygame.image.load(f"default/icons/wall.png")
        screen.blit(iconImage, (y * tileSize, 0))
        screen.blit(iconImage, (y * tileSize, (height + 1) * tileSize))


def spawnCreatures(screen: pygame.Surface, ghosts: list, pacmans: list, tileSize: int = 20):
    for ghost in ghosts:
        x, y = ghost.getCoordinates()
        iconImage = pygame.image.load(f"default/icons/ghost{ghost.getTeam()}.png")
        screen.blit(iconImage, ((y + 1)*tileSize, (x + 1)*tileSize))
    
    for pacman in pacmans:
        x, y = pacman.getCoordinates()
        iconImage = pygame.image.load(f"default/icons/pacman{pacman.getTeam()}.png")
        screen.blit(iconImage, ((y + 1)*tileSize, (x + 1)*tileSize))


def redrawBoard(screen: pygame.Surface, maze: maze.Maze, pacmans, ghosts, coordsOld: list[int], tileSize=20):
    for i, j in coordsOld:
        tile = maze.getNode(i, j)
        if tile.getTeam() == 0:
            drawTile(screen, tile)
    
    dots = maze.getDotsPosition()
    for di, dj in dots:
        tile = maze.getNode(di, dj)
        drawTile(screen, tile)

    for ghost in ghosts:
        x, y = ghost.getCoordinates()
        iconImage = pygame.image.load(f"default/icons/ghost{ghost.getTeam()}.png")
        screen.blit(iconImage, ((y + 1)*tileSize, (x + 1)*tileSize))
    
    for pacman in pacmans:
        x, y = pacman.getCoordinates()
        iconImage = pygame.image.load(f"default/icons/pacman{pacman.getTeam()}.png")
        screen.blit(iconImage, ((y + 1)*tileSize, (x + 1)*tileSize))

# def eatDot(self, maze)
