class Tile:
    def __init__(self):
        self.isFlagged = False
        self.isRevealed = False
        self.isMine = False
        self.adjacentMines = 0