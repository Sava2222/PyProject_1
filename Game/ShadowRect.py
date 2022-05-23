from Model import *
from Window import *


class ShadowRect(Model):
    def draw(self):
        pygame.draw.rect(Window.screen, (0, 0, 0),
                         (self.center_x - self.weight // 2,
                          self.center_y - self.height // 2,
                          self.weight, self.height))
