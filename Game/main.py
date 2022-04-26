import pygame
import sys
import time
pygame.init()

left_want_to_step = pygame.image.load('left_want_to_step.png')
left_step = pygame.image.load('left_step.png')
left_stop = pygame.image.load('left_stop.png')
right_want_to_step = pygame.image.load('right_want_to_step.png')
right_step = pygame.image.load('right_step.png')
right_stop = pygame.image.load('right_stop.png')
up_want_to_step = pygame.image.load('up_left_foot.png')
up_step = pygame.image.load('up_right_foot.png')
up_stop = pygame.image.load('up_stop.png')
down_left_arm = pygame.image.load('down_left_arm.png')
down_right_arm = pygame.image.load('down_right_arm.png')
down_stop = pygame.image.load('down_stop.png')
background_image = pygame.image.load('map.png')
left = [pygame.transform.scale(left_want_to_step, (70, 100)), pygame.transform.scale(left_step, (70, 100)),
        pygame.transform.scale(left_stop, (70, 100))]
right = [pygame.transform.scale(right_want_to_step, (70, 100)), pygame.transform.scale(right_step, (70, 100)),
         pygame.transform.scale(right_stop, (70, 100))]
up = [pygame.transform.scale(up_want_to_step, (70, 100)), pygame.transform.scale(up_step, (70, 100)),
      pygame.transform.scale(up_stop, (70, 100))]
down = [pygame.transform.scale(down_left_arm, (70, 100)), pygame.transform.scale(down_right_arm, (70, 100)),
        pygame.transform.scale(down_stop, (70, 100))]


class Window:
    weight = 1280
    height = 650
    size = [weight, height]
    colour = (235, 200, 148)
    fps = 10
    center_x = weight // 2
    center_y = height // 2
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()


class Model:
    center_x = int()
    center_y = int()
    height = int()
    weight = int()

    def __init__(self, center_x, center_y, weight, height):
        self.center_x = center_x
        self.center_y = center_y
        self.height = height
        self.weight = weight

    def draw(self):
        pass


class Chair(Model):
    chairs_counter = 0
    weight = 20
    height = 20

    def draw(self):
        pygame.draw.rect(Window.screen, (101, 67, 33),
                         (self.center_x - self.weight // 2, self.center_y - self.height // 2, self.weight, self.height))


class Hero(Model):
    weight = 70
    height = 100
    colour = (200, 100, 0)

    real_weight = 70
    real_height = 100

    have_chair = False
    speed = 8

    center_x = 815
    center_y = 530


def Near(a, b, dist):
    if abs(a.center_x - b.center_x) < a.weight // 2 + b.weight // 2 + dist and \
       abs(a.center_y - b.center_y) < a.height // 2 + b.height // 2 + dist:
        return True
    else:
        return False


class ShadowRect(Model):
    def draw(self):
        pygame.draw.rect(Window.screen, (0, 0, 0), (self.center_x - self.weight // 2, self.center_y - self.height // 2, self.weight, self.height))


shadow = ShadowRect(250, 152, 412, 232)


walls = list()
walls.append(Model(459, 395, 6, 510))
walls.append(Model(459, 18, 6, 36))
walls.append(Model(251, 34, 420, 6))
walls.append(Model(41, 156, 6, 230))
walls.append(Model(250, 270, 418, 6))
walls.append(Model(818, 237, 6, 474))
walls.append(Model(818, 622, 6, 56))
walls.append(Model(1006, 596, 376, 6))
walls.append(Model(1006, 338, 376, 6))
walls.append(Model(1193, 467, 6, 258))

chairs = [Chair(100, 100, 20, 20), Chair(200, 100, 20, 20)]

font = pygame.font.SysFont("", 24)
img = font.render('Press \'e\' to take chair', True, (255, 255, 255))
win_text = font.render('You won!', True, (255, 255, 255))

hero = Hero(815, 530, 52, 90)
last_act = str()
running = True
last_keys = [0, 0, 0, 0]
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    keys_pressed = pygame.key.get_pressed()
    Window.screen.blit(background_image, (0, 0))

    if keys_pressed[pygame.K_ESCAPE]:
        break
    if keys_pressed[pygame.K_UP] and not keys_pressed[pygame.K_LEFT]\
            and not keys_pressed[pygame.K_RIGHT] and \
            not keys_pressed[pygame.K_DOWN]:
        hero.center_y -= hero.speed
        last_act = 'up'
        for i in range(len(last_keys)):
            if i == 3:
                last_keys[i] += 1
            else:
                last_keys[i] = 0
    if keys_pressed[pygame.K_DOWN] and not keys_pressed[pygame.K_UP]\
            and not keys_pressed[pygame.K_LEFT] and \
            not keys_pressed[pygame.K_RIGHT]:
        hero.center_y += hero.speed
        last_act = 'down'
        for i in range(len(last_keys)):
            if i == 2:
                last_keys[i] += 1
            else:
                last_keys[i] = 0
    if keys_pressed[pygame.K_LEFT] and not keys_pressed[pygame.K_RIGHT]\
            and not keys_pressed[pygame.K_DOWN] and \
            not keys_pressed[pygame.K_UP]:
        hero.center_x -= hero.speed
        last_act = 'left'
        for i in range(len(last_keys)):
            if i == 0:
                last_keys[i] += 1
            else:
                last_keys[i] = 0
    if keys_pressed[pygame.K_RIGHT] and not keys_pressed[pygame.K_LEFT]\
            and not keys_pressed[pygame.K_UP] and \
            not keys_pressed[pygame.K_DOWN]:
        hero.center_x += hero.speed
        last_act = 'right'
        for i in range(len(last_keys)):
            if i == 1:
                last_keys[i] += 1
            else:
                last_keys[i] = 0
    if not keys_pressed[pygame.K_UP] and not keys_pressed[pygame.K_LEFT]\
            and not keys_pressed[pygame.K_RIGHT] and \
            not keys_pressed[pygame.K_DOWN]:
        for i in range(len(last_keys)):
            if last_keys[i]:
                last_keys[i] = 2
    hero.center_y = max(0, hero.center_y)
    hero.center_y = min(650 - hero.weight, hero.center_y)

    for i in walls:
        if Near(i, hero, 0):
            if last_act == 'up':
                hero.center_y += hero.speed
            if last_act == 'down':
                hero.center_y -= hero.speed
            if last_act == 'left':
                hero.center_x += hero.speed
            if last_act == 'right':
                hero.center_x -= hero.speed

    for chair in chairs:
        if Near(chair, hero, 10) and not hero.have_chair:
            Window.screen.blit(img, (550, 600))
            if keys_pressed[pygame.K_e]:
                chair.chairs_counter = True
                hero.have_chair = True
        if not chair.chairs_counter:
            chair.draw()

    if last_keys[0]:
        left[last_keys[0] % 3].set_colorkey((255, 255, 255))
        Window.screen.blit(left[last_keys[0] % 3], (hero.center_x - hero.real_weight // 2, hero.center_y - hero.real_height // 2))
    if last_keys[1]:
        right[last_keys[1] % 3].set_colorkey((255, 255, 255))
        Window.screen.blit(right[last_keys[1] % 3], (hero.center_x - hero.real_weight // 2, hero.center_y - hero.real_height // 2))
    if last_keys[2]:
        down[last_keys[2] % 3].set_colorkey((255, 255, 255))
        Window.screen.blit(down[last_keys[2] % 3], (hero.center_x - hero.real_weight // 2, hero.center_y - hero.real_height // 2))
    if last_keys[3]:
        up[last_keys[3] % 3].set_colorkey((255, 255, 255))
        Window.screen.blit(up[last_keys[3] % 3], (hero.center_x - hero.real_weight // 2, hero.center_y - hero.real_height // 2))

    if not Near(shadow, hero, 0):
        shadow.draw()

    if hero.have_chair and hero.center_x >= 820 and 570 >= hero.center_y >= 490:
        Window.screen.blit(win_text, (550, 600))
        pygame.display.update()
        time.sleep(3)
        running = False

    pygame.display.update()
    Window.clock.tick(Window.fps)
pygame.quit()
