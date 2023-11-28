#aboba
import math
import random
from random import choice

import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

#gravity
g = 200

#ball lifetime (number of cadrs)
ball_lifetime = 5 * FPS


class Ball:
    def __init__(self, screen: pygame.Surface, x, y):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """

        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30
        self.lifetime = 0

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        global FPS
        #inertion
        self.x += self.vx / FPS
        self.y -= self.vy / FPS

        #gravity
        self.vy -= g / FPS

        #colission with wall check

        if self.x > WIDTH or self.x < 0:
            self.vx *= -1
        if self.y > HEIGHT or self.y < 0:
            self.vy *= -1

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """

        distance = ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2) ** (1/2)
        if distance > (obj.r + self.r):
            return False
        return True

    def update_lifetime(self):
        self.lifetime += 1


#different types of balls
class Yellow_Ball(Ball):
    def __init__(self, screen, x, y):
        super().__init__(screen, x, y)
        self.color = YELLOW


class Blue_Ball(Ball):
    def __init__(self, screen, x, y):
        super().__init__(screen, x, y)
        self.color = BLUE


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 50
        self.y = 450
        self.vx0 = 150

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1

        ij = random.randint(1, 2)
        if ij == 1:
            new_ball = Yellow_Ball(self.screen, gun.x, gun.y)
        else:
            new_ball = Blue_Ball(self.screen, gun.x, gun.y)

        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an) * 10
        new_ball.vy = - self.f2_power * math.sin(self.an) * 10
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        sx = self.x
        sy = self.y
        pygame.draw.polygon(self.screen,
                            self.color,
                            ((sx, sy),
                             (sx + 5 * self.f2_power * math.cos(self.an), sy + 5 * self.f2_power * math.sin(self.an)),
                             (sx + 5 * self.f2_power * math.cos(self.an) - 20 * math.sin(self.an), sy + 5 * self.f2_power * math.sin(self.an) + 20 * math.cos(self.an)),
                             (sx - 20 * math.sin(self.an), sy + 20 * math.cos(self.an))))

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY

    def move_left(self):
        self.x -= self.vx0 / FPS

    def move_right(self):
        self.x += self.vx0 / FPS


class Target:
    def __init__(self):
        self.screen = screen
        self.points = 0
        self.live = 1
        x = self.x = random.randint(600, 780)
        y = self.y = random.randint(300, 550)
        r = self.r = random.randint(2, 50)
        self.vx = random.randint(0, 50)
        self.vy = random.randint(0, 50)
        color = self.color = RED

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def move(self):
        self.x += self.vx / FPS
        self.y += self.vy / FPS

        #colission with walls check

        if self.x > WIDTH or self.x < 0:
            self.vx *= -1
        if self.y > HEIGHT or self.y < 0:
            self.vy *= -1


#Цель, которая движется по окружности
class Rotating_Target(Target):
    def __init__(self):
        super().__init__()
        self.omega = random.randint(1, 10)

    def move(self):
        self.x += self.vx / FPS
        self.y += self.vy / FPS

        #rotation

        self.vx += self.vy * self.omega / FPS
        self.vy += self.vx * (-1) * self.omega / FPS

        # colission with walls check

        if self.x > WIDTH or self.x < 0:
            self.vx *= -1
        if self.y > HEIGHT or self.y < 0:
            self.vy *= -1


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target1 = Target()
target2 = Rotating_Target()
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target1.draw()
    target2.draw()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                gun.move_left()
            elif event.key == pygame.K_d:
                gun.move_right()

    target1.move()
    target2.move()

    for b in balls:
        b.move()
        b.update_lifetime()

        #check collisions
        if b.hittest(target1) and target1.live:
            target1.live = 0
            target1.hit()
            target1 = Target()

        if b.hittest(target2) and target2.live:
            target2.live = 0
            target2.hit()
            target2 = Rotating_Target()

    # remove old balls
    if len(balls) > 0 and balls[0].lifetime > ball_lifetime:
        balls.remove(balls[0])

    gun.power_up()

pygame.quit()