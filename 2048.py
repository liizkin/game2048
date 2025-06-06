import pygame
import numpy as np
import random


BG_COLORS = {
    0: (250, 250, 250),
    2: (220, 213, 204),
    4: (235, 224, 203),
    8: (232, 180, 129),
    16: (232, 154, 108),
    32: (230, 131, 103),
    64: (228, 104, 71),
    128: (232, 208, 127),
    256: (232, 205, 114),
    512: (231, 201, 101),
    1024: (227, 197, 89),
    2048: (226, 194, 78)
}


class Game_2048:
    def __init__(self):
        self.N = 4 
        self.cellSize = 100
        self.gap = 1
        self.windowBgColor = (245, 229, 143)
        self.blockSize = self.cellSize + self.gap * 2
        self.windowWidth = self.blockSize * 4 
        self.windowHeight = self.windowWidth

        pygame.init()
        self.window = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        pygame.display.set_caption('2048')

        self.boardStatus = np.zeros((self.N, self.N))
        self.addNewNumber()

    def addNewNumber(self):
        freePosition = zip(*np.where(self.boardStatus == 0))
        freePosition = list(freePosition)

        for position in random.sample(freePosition, k=1):
            self.boardStatus[position] = 2 

    def drawBoard(self):
        self.window.fill(self.windowBgColor)

        for i in range(self.N):
            rectY = self.blockSize * i + self.gap  
            for j in range(self.N):
                rectX = self.blockSize * j + self.gap 
                cellValue = int(self.boardStatus[i][j])     

                pygame.draw.rect(
                    self.window,
                    BG_COLORS[cellValue],
                    pygame.Rect(rectX, rectY, self.cellSize, self.cellSize)
                )

                if cellValue != 0:
                    textSurface = self.font.render(f'{cellValue}', True, (0, 0, 0))
                    textRect = textSurface.get_rect(center=(rectX + self.blockSize/2, rectY + self.blockSize/2))
                    self.window.blit(textSurface, textRect)

    def compressNumber(self, data):
        result = [0]
        data = [x for x in data if x != 0]
        for element in data:
            if element == result[len(result) - 1]:
                result[len(result) - 1] *= 2
                result.append(0)
            else:
                result.append(element)

        result = [x for x in result if x != 0]
        return result

    def move(self, char):
        for index in range(self.N):

            if char in 'ud':
                data = self.boardStatus[:, index]
            else:
                data = self.boardStatus[index, :]
            
            flip = False
            if char in 'rd':
                flip = True
                data = data[::-1]

            data = self.compressNumber(data)
            data = data + (self.N - len(data)) * [0]

            if flip:
                data = data[::-1]
            
            if char in 'ud':
                self.boardStatus[:, index] = data
            else:
                self.boardStatus[index, :] = data

    def isGameOver(self):
        boardStatusBackup = self.boardStatus.copy()
        for char in 'udlr':
            self.move(char)

            if (self.boardStatus == boardStatusBackup).all() == False:
                self.boardStatus = boardStatusBackup
                return False
        return True

    def play(self):
        running = True
        while running:
            self.drawBoard()
            pygame.display.update()

            for event in pygame.event.get():
                oldBoardStatus = self.boardStatus.copy()

                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.move('u')
                    elif event.key == pygame.K_DOWN:
                        self.move('d')
                    elif event.key == pygame.K_LEFT:
                        self.move('l')
                    elif event.key == pygame.K_RIGHT:
                        self.move('r')
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                    if self.isGameOver():
                        print('game over')
                        return

                    if (self.boardStatus == oldBoardStatus).all() == False:
                        self.addNewNumber()


if __name__ == '__main__':
    game = Game_2048()
    game.play() 
    