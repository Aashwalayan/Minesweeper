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

font = pygame.font.SysFont(None, 24)

def getRandNum():
    return random.randint(1, 10)

rowsOfTiles = 30
colsOfTiles = 30

grid = [[Tile() for _ in range(colsOfTiles)] for _ in range(rowsOfTiles)]

def createGrid(grid: list):

    for row in range (rowsOfTiles):
        for col in range(colsOfTiles):

            tile = grid[row][col]

            num = getRandNum()

            if num <= 2:
                tile.isMine = True
            
            
    return grid

def calculateNums(grid: list):
    for row in range(rowsOfTiles):
        for col in range(colsOfTiles):
            count = 0

            for i in range(-1, 2):
                for j in range(-1, 2):

                    newRow = row + i
                    newCol = col + j

                    if not(0 <= newRow < rowsOfTiles):
                        continue

                    if not(0 <= newCol < colsOfTiles):
                        continue

                    if i == 0 and j == 0:
                        continue

                    if grid[newRow][newCol].isMine:
                        count += 1

            grid[row][col].adjacentMines = count


tileSize = 30



def updateBoardPositions():

    boardWidth = colsOfTiles * tileSize
    boardHeight = rowsOfTiles * tileSize

    offsetX = (screen.get_width() - boardWidth) // 2
    offsetY = (screen.get_height() - boardHeight) // 2

    return offsetX, offsetY, boardHeight, boardWidth

def drawBoard(screen, grid: list, offsetX, offsetY, boardWidth, boardHeight, gameOver):

    
    
    for row in range(rowsOfTiles):
        for col in range(colsOfTiles):
            
            tile = grid[row][col]
            border = 0

            
            
            x = offsetX + tileSize * col
            y = offsetY + tileSize * row


            if tile.isMine and gameOver:
                color = (0, 0, 0)

            else:
                if tile.isFlagged and not tile.isRevealed:
                    color = (200, 0, 0)
                    border = 1

                elif tile.isRevealed and not tile.isMine and not tile.isFlagged:
                    color = (255, 255, 50)
                    border = 0

                    if tile.adjacentMines > 0:
                        mineNum = tile.adjacentMines
                        mineNumColor = (0, 0, 0)
                        
                        match mineNum:
                            case 1:
                                mineNumColor = (0, 0, 255)      # blue
                            case 2:
                                mineNumColor = (0, 128, 0)      # green
                            case 3:
                                mineNumColor = (255, 0, 0)      # red
                            case 4:
                                mineNumColor = (0, 0, 128)
                            case 5:
                                mineNumColor = (128, 0, 0)
                            case 6:
                                mineNumColor = (0, 128, 128)
                            case 7:
                                mineNumColor = (0, 0, 0)
                            case 8:
                                mineNumColor = (128, 128, 128)
                    
                        text = font.render(str(mineNum), True, mineNumColor)
                    
                        textRect = text.get_rect(
                            center = (x + tileSize // 2, y + tileSize // 2)
                        )

                        screen.blit(text, textRect)

                else:
                    color = (200, 200, 200)
                    border = 0

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

            pygame.draw.rect(
            screen,
            (255, 0, 0),
            (offsetX - 5, offsetY - 5, boardHeight + 10, boardWidth + 10),
            2
            )

createGrid(grid)
calculateNums(grid)

gameOver = False

running = True

while running:
    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            
            if (offsetX <= mouseX < offsetX + boardWidth and offsetY <= mouseY < offsetY + boardHeight):

                tileX = (mouseX - offsetX) // tileSize
                tileY = (mouseY - offsetY) // tileSize

                clickedTile = grid[tileY][tileX]

                if event.button == 1:
                    clickedTile.isRevealed = True

                    if clickedTile.isMine:
                        gameOver = True

                elif event.button == 3:
                    if not clickedTile.isRevealed:
                        clickedTile.isFlagged = not clickedTile.isFlagged


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
    offsetX, offsetY, boardHeight, boardWidth = updateBoardPositions()
    drawBoard(screen, grid, offsetX, offsetY, boardWidth, boardHeight, gameOver)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()
