import pygame


# A model that is inherited by other classes


class Model:
    def __init__(self, center_x, center_y, weight, height):
        self.center_x = center_x
        self.center_y = center_y
        self.height = height
        self.weight = weight

    def draw(self):
        pass

    def is_near(self, b, dist):
        if abs(self.center_x - b.center_x) < self.weight // 2 + b.weight // 2 + dist and \
                abs(self.center_y - b.center_y) < self.height // 2 + b.height // 2 + dist:
            return True
        else:
            return False
