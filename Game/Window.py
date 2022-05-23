import pygame


class Window:
    @staticmethod
    def set_mode():
        return pygame.display.set_mode(Window.size)

    @staticmethod
    def start_clock():
        return pygame.time.Clock()

    weight = 1280
    height = 650
    size = [weight, height]
    colour = (235, 200, 148)
    fps = 10
    center_x = weight // 2
    center_y = height // 2

    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()


