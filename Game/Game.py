import sys
import pygame.font
from Button import *
from Chair import *
from ShadowRect import *
from Hero import *
from Window import *
import time
import random


class Game:
    def font_render(self):
        self.font = pygame.font.SysFont("", 24)
        self.menu_text = pygame.font.SysFont('Helvetica', size=70)

    def make_text(self):
        self.near_chair_text = self.font.render('Press \'e\' to take chair', True, (255, 255, 255))
        self.win_text = self.font.render('You won!', True, (255, 255, 255))
        self.play_text = self.menu_text.render('PLAY', True, (255, 255, 255))
        self.exit_text = self.menu_text.render('EXIT', True, (255, 255, 255))

    def __init__(self):
        self.walls = list()
        self.font_render()
        self.make_text()
        self.shadows = [ShadowRect(250, 466, 412, 232), ShadowRect(250, 152, 412, 232),
                        ShadowRect(1027, 151, 412, 232), ShadowRect(1027, 466, 412, 232)]
        self.hero = Hero(815, 530, 52, 90)
        self.moving_keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
        self.actions_names = ['left', 'right', 'up', 'down']
        self.last_act = str()
        self.keys_pressed = []
        self.running = True
        self.last_keys = [0, 0, 0, 0]
        self.back_hero_colour = (255, 255, 255)
        self.back_menu_colour = (255, 255, 255)
        self.image_size = (70, 100)
        self.button_exit = Button(self.exit_text, 400, 200)
        self.button_play = Button(self.play_text, 400, 200)

        self.room_coordinates = [(43, 350), (43, 36), (821, 36), (821, 350)]
        self.relative_chair_coordinates = [(30, 30), (90, 30), (150, 30), (210, 30), (270, 30), (330, 30),
                                           (30, 90), (90, 90), (150, 90), (210, 90), (270, 90), (330, 90)]
        self.areas_forward = [[self.generate_room(self.room_coordinates[i]) for i in range(3)]]
        self.areas_backward = [[self.generate_room(self.room_coordinates[i]) for i in range(4)]]

    def transform(self, image_of_step_type, size):
        return pygame.transform.scale(image_of_step_type, size)

    @staticmethod
    def image_load(source):
        return pygame.image.load(source)

    def upload_images(self):
        self.left_want_to_step = Game.image_load('left_want_to_step.png')
        self.left_step = Game.image_load('left_step.png')
        self.left_stop = Game.image_load('left_stop.png')
        self.right_want_to_step = Game.image_load('right_want_to_step.png')
        self.right_step = Game.image_load('right_step.png')
        self.right_stop = Game.image_load('right_stop.png')
        self.up_want_to_step = Game.image_load('up_left_foot.png')
        self.up_step = Game.image_load('up_right_foot.png')
        self.up_stop = Game.image_load('up_stop.png')
        self.down_left_arm = Game.image_load('down_left_arm.png')
        self.down_right_arm = Game.image_load('down_right_arm.png')
        self.down_stop = Game.image_load('down_stop.png')
        self.background_image = Game.image_load('map.png')
        self.back_menu = Game.image_load('back_menu.png')

        self.first_room = Game.image_load('map1.png')
        self.second_room = Game.image_load('map2.png')
        self.free_chair = self.transform(Game.image_load('chair.png'), (25, 30))
        self.busy_chair = self.transform(Game.image_load('busy_chair.png'), (45, 50))

    def render_walls(self):
        self.walls.append(Model(459, 309, 6, 334))
        self.walls.append(Model(459, 18, 6, 36))
        self.walls.append(Model(459, 616, 6, 68))

        self.walls.append(Model(818, 309, 6, 334))
        self.walls.append(Model(818, 18, 6, 36))
        self.walls.append(Model(818, 616, 6, 68))

        self.walls.append(Model(251, 34, 420, 6))
        self.walls.append(Model(41, 156, 6, 230))
        self.walls.append(Model(250, 270, 418, 6))

        self.walls.append(Model(1027, 34, 418, 6))
        self.walls.append(Model(1235, 156, 6, 230))
        self.walls.append(Model(1027, 270, 418, 6))

        self.walls.append(Model(250, 347, 418, 6))
        self.walls.append(Model(250, 584, 418, 6))
        self.walls.append(Model(41, 466, 6, 230))

        self.walls.append(Model(1027, 347, 418, 6))
        self.walls.append(Model(1235, 466, 6, 230))
        self.walls.append(Model(1027, 584, 418, 6))

    def make_list(self, first_photo, second_photo, third_photo):
        return [self.transform(first_photo, self.image_size), self.transform(second_photo, self.image_size),
                self.transform(third_photo, self.image_size)]

    def init_moving_images(self):
        self.left = self.make_list(self.left_want_to_step, self.left_step, self.left_stop)
        self.right = self.make_list(self.right_want_to_step, self.right_step, self.right_stop)
        self.up = self.make_list(self.up_want_to_step, self.up_step, self.up_stop)
        self.down = self.make_list(self.down_left_arm, self.down_right_arm, self.down_stop)
        self.directions = [self.left, self.right, self.up, self.down]

    def start(self):
        self.font_render()
        self.upload_images()
        self.render_walls()
        self.init_moving_images()
        self.render_walls()
        self.make_text()

    def change_pictures(self, direction_key):
        self.directions[direction_key][self.last_keys[direction_key] % 3].set_colorkey(self.back_hero_colour)
        Window.screen.blit(self.directions[direction_key][self.last_keys[direction_key] % 3],
                           (self.hero.center_x - self.hero.real_weight // 2,
                            self.hero.center_y - self.hero.real_height // 2))

    def moving(self):
        count_of_pressed = 0
        pressed_key = -1
        for i in range(len(self.moving_keys)):
            for j in range(len(self.moving_keys)):
                if self.keys_pressed[self.moving_keys[i]] and i != j and \
                        self.keys_pressed[self.moving_keys[j]]:
                    count_of_pressed = 2
                    break
            if self.keys_pressed[self.moving_keys[i]] and count_of_pressed == 0:
                pressed_key = i
                count_of_pressed = 1
                break
        if count_of_pressed == 1:
            self.last_act = self.actions_names[pressed_key]
            if pressed_key == 0:
                self.hero.center_x -= self.hero.speed
            elif pressed_key == 1:
                self.hero.center_x += self.hero.speed
            elif pressed_key == 2:
                self.hero.center_y -= self.hero.speed
            else:
                self.hero.center_y += self.hero.speed
            self.last_keys[pressed_key] += 1
            for k in range(len(self.moving_keys)):
                if k != pressed_key:
                    self.last_keys[k] = 0
        else:
            for i in range(len(self.last_keys)):
                if self.last_keys[i]:
                    self.last_keys[i] = 2
                else:
                    self.last_keys[i] = 0

    def generate_room(self, coord):
        new_room = []
        if random.randint(1, 100) < 80:
            for i in self.relative_chair_coordinates:
                new_room.append(Chair(coord[0] + i[0], coord[1] + i[1], 20, 20))
                new_room[len(new_room) - 1].is_busy = True
        else:
            for i in self.relative_chair_coordinates:
                new_room.append(Chair(coord[0] + i[0], coord[1] + i[1], 20, 20))
                if random.randint(1, 100) < 80:
                    new_room[len(new_room) - 1].is_busy = True

        return new_room

    def change_position_forward(self):
        self.hero.position += 1
        if self.hero.position == len(self.areas_forward):
            self.areas_forward.append([self.generate_room(self.room_coordinates[i]) for i in range(4)])

    def change_position_backward(self):
        self.hero.position -= 1
        if self.hero.position == -len(self.areas_backward):
            self.areas_backward.append([self.generate_room(self.room_coordinates[i]) for i in range(4)])

    def show_menu(self):
        Window.screen.blit(self.back_menu, (0, 0))
        self.button_play.draw_button(Window.weight // 2 - 200, Window.height // 2 - 250)
        self.button_exit.draw_button(Window.weight // 2 - 200, Window.height // 2 + 50)
        if self.button_exit.exit == 1:
            self.running = 0
            pygame.quit()
        Window.screen.blit(self.play_text, (Window.weight // 2 - 90, Window.height // 2 - 180))
        Window.screen.blit(self.exit_text, (Window.weight // 2 - 80, Window.height // 2 + 120))
        pygame.display.update()

    def win(self):
        Window.screen.blit(self.win_text, (550, 600))
        pygame.display.update()
        time.sleep(5)
        sys.exit()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        self.keys_pressed = pygame.key.get_pressed()
        self.moving()

        for i in self.walls:
            if self.hero.is_near(i, 0):
                if self.last_act == 'up':
                    self.hero.center_y += self.hero.speed
                if self.last_act == 'down':
                    self.hero.center_y -= self.hero.speed
                if self.last_act == 'left':
                    self.hero.center_x += self.hero.speed
                if self.last_act == 'right':
                    self.hero.center_x -= self.hero.speed

        if self.hero.have_chair and self.hero.center_x >= 820 and 570 >= self.hero.center_y >= 490 and \
                self.hero.position == 0:
            self.win()

        # self.hero.center_y = max(0, self.hero.center_y)
        # self.hero.center_y = min(650 - self.hero.weight, self.hero.center_y)
        if self.hero.center_y <= 0:
            self.change_position_forward()
        if self.hero.center_y >= 650:
            self.change_position_backward()
        self.hero.center_y %= 650

        if self.keys_pressed[pygame.K_ESCAPE]:
            self.button_play.exit = 0

    def draw(self):
        # Window.screen.blit(self.background_image, (0, 0))
        if self.hero.position % 2 == 0:
            Window.screen.blit(self.first_room, (0, 0))
        else:
            Window.screen.blit(self.second_room, (0, 0))

        if self.hero.position >= 0:
            rooms = self.areas_forward[self.hero.position]
        else:
            rooms = self.areas_backward[-self.hero.position]

        for room in rooms:
            for chair in room:
                if self.hero.is_near(chair, 10) and not self.hero.have_chair and not chair.is_busy:
                    Window.screen.blit(self.near_chair_text, (550, 600))
                    if self.keys_pressed[pygame.K_e]:
                        self.hero.have_chair = True
                        chair.was_got = True

                if not chair.was_got:
                    if chair.is_busy:
                        Window.screen.blit(self.busy_chair, (chair.center_x - chair.weight // 2,
                                                             chair.center_y - chair.height // 2))
                        self.busy_chair.set_colorkey(self.back_hero_colour)
                    else:
                        Window.screen.blit(self.free_chair, (chair.center_x - chair.weight // 2,
                                                             chair.center_y - chair.height // 2))
                        self.free_chair.set_colorkey(self.back_hero_colour)

        for i in range(0, len(self.shadows) - 1):
            if not self.hero.is_near(self.shadows[i], 0):
                self.shadows[i].draw()
        if self.hero.position != 0 and not self.hero.is_near(self.shadows[len(self.shadows) - 1], 0):
            self.shadows[len(self.shadows) - 1].draw()

        for i in range(len(self.last_keys)):
            if self.last_keys[i]:
                self.change_pictures(i)

        if self.button_play.exit == 0:
            self.show_menu()

    def run(self):
        while self.running:
            self.update()
            self.draw()

            pygame.display.update()
            Window.clock.tick(Window.fps)

