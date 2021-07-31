import os
import time
import numpy as np
from numpy.core.shape_base import block
import pygame
import random

pygame.init()

FPS = 10
# x is along width y is along height
TOP_WIDTH = 100
WIDTH, HEIGHT = 20, 20   #GRID SIZE
BLOCK_SIZE = 20
SIZE_X, SIZE_Y = WIDTH*BLOCK_SIZE, HEIGHT*BLOCK_SIZE + TOP_WIDTH  #WINDOW SIZE
WIN = pygame.display.set_mode((SIZE_X, SIZE_Y))
pygame.display.set_caption("Game of Life -- Conway")
BUTTON_WIDTH, BUTTON_HEIGHT = 100, 30
FONT = pygame.font.SysFont("comicsans", 30 )
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Button:
    def __init__(self, text, x, y, color = "lightblue", color2 = "green"):
        self.x, self.y = x, y
        self.text = FONT.render(text, 1, pygame.Color("Black"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.rect = pygame.Rect(x, y, self.size[0], self.size[1])
        self.color = pygame.Color(color)
        self.color2 = color2
        self.surface.fill(self.color)
    def select(self, x, y):
        if self.rect.collidepoint(x, y):
            self.color = self.color2
            self.surface.fill(self.color2)
            return True;
    def show(self):
        WIN.blit(self.surface, (self.x, self.y))
        WIN.blit(self.text, (self.x, self.y))


class Start_Button(Button):
    def select(self, x, y):
        if self.rect.collidepoint(x, y):
            temp = self.color
            self.color = self.color2
            self.color2 = temp
            self.surface.fill(self.color2)
            return True;

class Board:
    def __init__(self, width, height, initial_states = []):
        self.height = height
        self.width = width
        self.board = np.zeros((height+2, width+2), dtype=np.uint)
        for i in initial_states:
            self.board[i[0], i[1]] = 1
    def reset(self):
        self.board = np.zeros((self.height+2, self.width+2), dtype=np.uint)
    def set_random_initial_state(self, n = WIDTH*HEIGHT//5):
        initial_states = []
        for _ in range(n):
            initial_states.append((random.randint(1, HEIGHT), random.randint(1, WIDTH)))
        for i in initial_states:
            self.board[i[0], i[1]] = 1
    def user_set(self, x, y):
        posx, posy = x//BLOCK_SIZE, (y - TOP_WIDTH)//BLOCK_SIZE 
        if posx >= 0 and posx < self.width and posy >= 0 and posy < self.height:
            self.board[posy+1, posx+1] = 1
    def update(self):
        curr = self.board.copy()
        for i in range(1, self.height):
            for j in range(1, self.width):
                if self.live(i, j):
                    curr[i, j] = 1
                else:
                    curr[i, j] = 0
        self.board = curr
    def live(self, i, j):
        neighbours = 0
        dir = {-1, 0, 1}
        for dx in dir:
            for dy in dir:
                neighbours += self.board[i+dx, j+dy]
        neighbours -= self.board[i, j]
        if self.board[i, j] == 1 and (neighbours == 2 or neighbours == 3):
            return True
        elif self.board[i, j] == 0 and neighbours == 3:
            return True
        else:
            return False        
    def draw_window(self, buttons = []):
            WIN.fill(WHITE)
            self.draw_grid()
            for button in buttons:
                button.show()
            pygame.display.update()
    def draw_grid(self):
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x*BLOCK_SIZE, TOP_WIDTH + y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                if self.board[y+1, x+1] == 1:
                    pygame.draw.rect(WIN, BLACK, rect)
                pygame.draw.rect(WIN, BLACK, rect, 1)


def main():
    board = Board(WIDTH, HEIGHT)
    button_random = Button("Random", 10, (TOP_WIDTH-BUTTON_HEIGHT)//2 )    
    button_start = Start_Button("Start/Stop", (SIZE_X-BUTTON_WIDTH)//2, (TOP_WIDTH-BUTTON_HEIGHT)//2, "green", "red")    
    button_quit = Button("Quit", SIZE_X-BUTTON_WIDTH-10, (TOP_WIDTH-BUTTON_HEIGHT)//2, "red" )    
    button_reset = Button("Reset", SIZE_X-2*BUTTON_WIDTH-20, (TOP_WIDTH-BUTTON_HEIGHT)//2, "purple", "purple")    
    buttons = [button_random, button_start, button_quit, button_reset]
    clock = pygame.time.Clock()
    
    run = True
    play = False
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                play = not play
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                board.user_set(x, y)
                if button_quit.select(x, y):
                    run = False
                    pygame.quit()
                if button_random.select(x, y):
                    board.set_random_initial_state()
                if button_start.select(x, y):
                    play = not play
                if button_reset.select(x, y):
                    board.reset()
        board.draw_window(buttons)
        if play:
            board.update()

main()   
