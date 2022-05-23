from Area import Area
import Game
import Window


class Corridor:
    position = 0
    areas = []
    first_room = Game.image_load('map1.png')
    second_room = Game.image_load('map2.png')

    def draw(self):
        if self.areas[self.position].room_type == 0:
            Window.screen.blit(self.first_room, (0, 0))
        else:
            Window.screen.blit(self.second_room, (0, 0))

        self.areas[self.position].draw()

    def add_area_to_end(self):
        self.areas.append(Area(1 - self.areas[len(self.areas) - 1].area_type))

    def add_area_to_begin(self):
        self.areas.insert(0, Area(1 - self.areas[0].area_type))
        self.position += 1
