import pygame
import sys
import random
from tile import Tile

pygame.init()

WIDTH, HEIGHT = 800, 600
fullscreen = False

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

clock = pygame.time.Clock()

def getRandNum():
    return random.randint(1, 10)


grid = [[Tile() for _ in range(20)] for _ in range(20)]

def createGrid(grid: list):

    for row in range (20):
        for col in range(20):

            tile = grid[row][col]

            num = getRandNum()

            if num <= 2:
                tile.isMine = True
            
            
    return grid



def drawBoard(screen, grid: list):
    tileSize = 30
    offsetX = 90
    offsetY = 90

    for row in range(20):
        for col in range(20):

            x = offsetX + tileSize * col
            y = offsetY + tileSize * row

            tile = grid[row][col]

            if tile.isMine :
                color = (255, 0, 0)
            else:
                color = (200, 200, 200)

            pygame.draw.rect(
                screen,
                color,
                (x, y, tileSize, tileSize)
            )

            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (x, y, tileSize, tileSize),
                2
            )

createGrid(grid)
            
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                fullscreen = not fullscreen

                if fullscreen:
                    screen = pygame.display.set_mode(
                        (0, 0), pygame.FULLSCREEN
                    )
                else:
                    screen = pygame.display.set_mode(
                        (WIDTH, HEIGHT)
                    )

    screen.fill((30, 30, 30))
    drawBoard(screen, grid)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()
