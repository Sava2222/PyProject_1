from Model import *
from Window import *
from Window import Window


class Chair(Model):
    chairs_counter = 0
    weight = 20
    height = 20
    coordinates = (101, 67, 33)
    is_busy = False
    was_got = False


    def draw(self):
        pygame.draw.rect(Window.screen, self.coordinates,
                         (self.center_x - self.weight // 2,
                          self.center_y - self.height // 2,
                          self.weight, self.height))
