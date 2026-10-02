import pygame
import sys
import random
from tile import Tile

pygame.init()

BG          = (34, 38, 46)      # window background
FRAME       = (60, 66, 78)      # board outline
HIDDEN      = (88, 101, 120)    # unrevealed tile
HIDDEN_HOVER= (106, 120, 141)
REVEALED    = (222, 217, 205)   # revealed tile
FLAG        = (224, 108, 117)
MINE_BG     = (70, 74, 86)
MINE_HIT    = (214, 100, 100)

NUMBER_COLORS = {
    1: (74, 120, 196), 2: (84, 150, 100), 3: (206, 92, 92),
    4: (110, 90, 170), 5: (170, 100, 70), 6: (60, 150, 150),
    7: (80, 80, 90),   8: (130, 130, 140),
}

font = pygame.font.SysFont("segoeui,helvetica,arial", 26, bold=True)
numFont = pygame.font.SysFont("segoeui,helvetica,arial", 20, bold=True)

WIDTH, HEIGHT = 800, 600
fullscreen = False

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

clock = pygame.time.Clock()


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

    mouseX, mouseY = pygame.mouse.get_pos()

    pygame.draw.rect(
            screen,
            FRAME,
            (offsetX - 8, offsetY - 8, boardWidth + 16, boardHeight + 16),
            2, border_radius=4
            )
    
    
    for row in range(rowsOfTiles):
        for col in range(colsOfTiles):
            
            tile = grid[row][col]
            x = offsetX + tileSize * col
            y = offsetY + tileSize * row
            rect = pygame.Rect(x, y, tileSize, tileSize).inflate(-2, -2)
            center = rect.center
            

            if tile.isMine and gameOver:
                pygame.draw.rect(screen, MINE_HIT if tile.isRevealed else MINE_BG, rect, border_radius=5)
                pygame.draw.circle(screen, (25, 25, 30), center, tileSize // 5)

            elif tile.isRevealed:
                pygame.draw.rect(screen, REVEALED, rect, border_radius=5)

                if tile.adjacentMines > 0:
                    text = numFont.render(str(tile.adjacentMines), True, NUMBER_COLORS[tile.adjacentMines])
                    screen.blit(text, text.get_rect(center=center))
            else:
                hovered = rect.collidepoint(mouseX, mouseY) and not gameOver
                pygame.draw.rect(screen, HIDDEN_HOVER if hovered else HIDDEN, rect, border_radius=5)

                if tile.isFlagged:
                    cx, cy = center
                    pygame.draw.line(screen, (240, 240, 240), (cx - 3, cy - 7), (cx - 3, cy + 7), 2)
                    pygame.draw.polygon(screen, FLAG, [(cx - 3, cy - 7), (cx + 7, cy - 3), (cx - 3, cy + 1)])

def revealFreeTiles(grid: list, row, col):

    tile = grid[row][col]

    if tile.isRevealed:
        return
    
    if tile.isMine:
        return
    
    tile.isRevealed = True

    if tile.adjacentMines > 0:
        return
    
    for i in range(-1, 2):
        for j in range(-1, 2):

            if i == 0 and j == 0:
                continue

            newRow = row + i
            newCol = col + j

            if not (0 <= newRow < rowsOfTiles):
                continue

            if not (0 <= newCol < colsOfTiles):
                continue

            revealFreeTiles(grid, newRow, newCol)


def placeMines(grid, count):
    
    while count > 0:
        
        rowI = random.randint(0, rowsOfTiles - 1)
        colJ = random.randint(0, colsOfTiles - 1)

        if grid[rowI][colJ].isMine:
            continue
        else:
            grid[rowI][colJ].isMine = True
            count -= 1

def checkWin(grid):
    for row in range(rowsOfTiles):
        for col in range(colsOfTiles):

            tile = grid[row][col]

            if not tile.isRevealed and not tile.isMine:
                return False
            
    return True

def resetGame():
    global grid, gameOver, gameWon, firstClick

    grid = [[Tile() for _ in range(colsOfTiles)] for _ in range(rowsOfTiles)]

    createGrid(grid)
    calculateNums(grid)

    gameOver = False
    gameWon = False
    firstClick = True

createGrid(grid)
calculateNums(grid)

gameOver = False
gameWon = False
firstClick = True
running = True

while running:
    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN and not gameOver and not gameWon:
            mouseX, mouseY = pygame.mouse.get_pos()
            
            if (offsetX <= mouseX < offsetX + boardWidth and offsetY <= mouseY < offsetY + boardHeight):

                tileX = (mouseX - offsetX) // tileSize
                tileY = (mouseY - offsetY) // tileSize

                clickedTile = grid[tileY][tileX]



                if event.button == 1:
                    
                    if firstClick:
                        firstClick = False

                        if clickedTile.isMine:
                            clickedTile.isMine = False
                            calculateNums(grid)

                        if clickedTile.adjacentMines > 0:
                            
                            mineCount = 0

                            for i in range(-1, 2):
                                for j in range(-1, 2):
                                    if i == 0 and j == 0:
                                        continue

                                    newRow = i + tileY
                                    newCol = j + tileX

                                    if not (0 <= newRow < rowsOfTiles):
                                        continue

                                    if not (0 <= newCol < colsOfTiles):
                                        continue

                                    if grid[newRow][newCol].isMine:
                                        grid[newRow][newCol].isMine = False
                                        
                                        mineCount += 1

                            placeMines(grid, mineCount)
                            calculateNums(grid)

                    if clickedTile.isMine:
                        clickedTile.isRevealed = True
                        gameOver = True

                    else:
                        revealFreeTiles(grid, tileY, tileX)

                        if checkWin(grid):
                            gameWon = True

                elif event.button == 3:
                    if not clickedTile.isRevealed:
                        clickedTile.isFlagged = not clickedTile.isFlagged


        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:
                resetGame()

            elif event.key == pygame.K_F11:
                fullscreen = not fullscreen

                if fullscreen:
                    screen = pygame.display.set_mode(
                        (0, 0), pygame.FULLSCREEN
                    )
                else:
                    screen = pygame.display.set_mode(
                        (WIDTH, HEIGHT)
                    )
        

    screen.fill(BG)
    offsetX, offsetY, boardHeight, boardWidth = updateBoardPositions()
    drawBoard(screen, grid, offsetX, offsetY, boardWidth, boardHeight, gameOver)

    if gameWon or gameOver:
        msg = "You Won!" if gameWon else "You Lost!"
        label = font.render(f"{msg} (Press R to restart)", True, (230, 230, 235))
        screen.blit(label, label.get_rect(center=(screen.get_width() // 2, offsetY + boardHeight + 30)))


    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()
