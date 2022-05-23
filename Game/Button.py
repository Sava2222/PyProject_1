from Game import *
from Window import *
import pygame


class Button:
    def __init__(self, text, weight=100, height=100):
        self.colour_touched_button = (128, 128, 128)
        self.colour_button = (170, 170, 170)
        self.weight = weight
        self.height = height
        self.menu = 0
        self.exit = 0
        self.text = text

    def draw_button(self, x, y):
        self.mouse_pos = pygame.mouse.get_pos()
        self.is_click = pygame.mouse.get_pressed()
        if x < self.mouse_pos[0] < x + self.weight and y < self.mouse_pos[1] < y + self.height:
            pygame.draw.rect(Window.screen, self.colour_button,
                             (x, y, self.weight, self.height))
            if self.is_click[0] or self.is_click[1]:
                pygame.time.delay(300)
                self.exit = 1
        else:
            pygame.draw.rect(Window.screen, self.colour_touched_button,
                             (x, y, self.weight, self.height))


