# Visualization of playing board
# Imports
import pygame
import maze


def drawTile(screen: pygame.Surface, tile, x, y, tileSize: int = 20):
    states = {0: 'free', 1: 'wall', 2: 'dot', 3: 'dot'}
    team = tile - 1
    if team < 1:
        team = ''
    iconImage = pygame.image.load(f"default/icons/{states[tile]}{team}.png")
    screen.blit(iconImage, ((y + 1) * tileSize, (x + 1) * tileSize))
    

def initBoard(maze: maze.Maze, screen: pygame.Surface, width: int, height: int, tileSize: int = 20):
    screen.fill((0, 0, 0))
    for x in range(height):
        for y in range(width):
            tile = maze.maze[x][y]
            drawTile(screen, tile, x, y, tileSize)

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
        x, y = ghost[0], ghost[1]
        iconImage = pygame.image.load(f"default/icons/ghost{ghost[2]}.png")
        screen.blit(iconImage, ((y + 1)*tileSize, (x + 1)*tileSize))
    
    for pacman in pacmans:
        x, y = pacman[0], pacman[1]
        iconImage = pygame.image.load(f"default/icons/pacman{pacman[2]}.png")
        screen.blit(iconImage, ((y + 1)*tileSize, (x + 1)*tileSize))


def redrawBoard(screen: pygame.Surface, maze: maze.Maze, pacmans, ghosts, coordsOld: list[int], tileSize=20):
    for i, j in coordsOld:
        tile = maze.maze[i][j]
        if tile in [0,1]:
            drawTile(screen, tile, i, j, tileSize)
    
    dots = maze.dotsPosition
    for di, dj in dots:
        tile = maze.maze[di][dj]
        drawTile(screen, tile, di, dj, tileSize)

    for ghost in ghosts:
        x, y = ghost[0], ghost[1]
        iconImage = pygame.image.load(f"default/icons/ghost{ghost[2]}.png")
        screen.blit(iconImage, ((y + 1)*tileSize, (x + 1)*tileSize))
    
    for pacman in pacmans:
        x, y = pacman[0], pacman[1]
        iconImage = pygame.image.load(f"default/icons/pacman{pacman[2]}.png")
        screen.blit(iconImage, ((y + 1)*tileSize, (x + 1)*tileSize))

# def eatDot(self, maze)
