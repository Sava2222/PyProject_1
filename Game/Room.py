import random
import Chair


class Room:
    relative_chair_coordinates = []
    chairs = []

    def __init__(self, x, y):
        if random.randint(1, 100) < 80:
            for i in self.relative_chair_coordinates:
                self.chairs.append(Chair.Chair(x + i[0], y + i[1], 20, 20))
                self.chairs[len(self.chairs) - 1].is_busy = True
        else:
            for i in self.relative_chair_coordinates:
                self.chairs.append(Chair.Chair(x + i[0], y + i[1], 20, 20))
                if random.randint(1, 100) < 80:
                    self.chairs[len(self.chairs) - 1].is_busy = True
