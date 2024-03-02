# Visualization of playing board
import pygame
import nodeStates
import resizeImages

# resizeImages.resizeImages()

def drawTile(screen: pygame.Surface, x: int, y: int, icon: nodeStates.State) -> None:
    iconImage = pygame.image.load(f"src/icons/{str(icon)}.png")
    screen.blit(iconImage, (x, y))

def drawBoard(screen: pygame.Surface, width: int, height: int, icon: nodeStates.State, tileSize: int = 20):
    pygame.init()
    screen = pygame.display.set_mode((width * tileSize, height * tileSize))
    pygame.display.set_caption("Pacman")

    for i in range(width):
        for j in range(height):
            iconImage = pygame.image.load(f"src/icons/{str(icon)}.png")
            screen.blit(iconImage, (x, y))
            # drawTile(screen, i * tileSize, j * tileSize, icon)
    pygame.display.flip()
