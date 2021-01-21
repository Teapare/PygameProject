import pygame
import random
FAKE_GRAVITY = 200  # px/sec
BRICK_SPAWN_INTERVAL = 3000  # ms
brick_spawn_counter = 2000  # ms


def attempt_obstacle_spawn(t):
    global brick_spawn_counter
    brick_spawn_counter += t
    if brick_spawn_counter > BRICK_SPAWN_INTERVAL:
        brick_spawn_counter %= 100
        Obstacle(random.randrange(1, 1401), -124)


class Brick(pygame.sprite.Sprite):
    image = pygame.image.load('Images/VeryLongBrick.png')

    def __init__(self, x, y):
        super(Brick, self).__init__(bricks)
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

    def update(self, *args, **kwargs) -> None:
        self.y += FAKE_GRAVITY * t / 1000
        if self.y > 900:
            self.kill()
        self.rect.y = self.y


class Obstacle:
    def __init__(self, x, y):
        self.left_brick = Brick(x - 1366, y)
        self.right_brick = Brick(x + 400, y)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load('Images/YEP_Emote_Banner.png')
        self.image = pygame.transform.scale(self.image, (100, 200))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 700
        self.x = 0
        self.orientation = 1
        self.velocity = 0
        self.v = 0
        self.slow_down = True

    def move(self, direction):
        self.velocity += direction * self.orientation * t / 1000 * 3000
        if self.velocity < 0:
            self.velocity *= -1
            self.orientation *= -1
            self.image = pygame.transform.flip(self.image, True, False)
        if self.velocity > 800:
            self.velocity = 800
        self.slow_down = False

    def check_collision(self):
        if pygame.sprite.spritecollideany(self, bricks):
            print('game over')
            global running
            running = False

    def update(self, time) -> None:
        if self.slow_down:
            self.velocity -= time * 2400
            if self.velocity < 0:
                self.velocity = 0
        self.x += time * self.velocity * self.orientation
        if self.x < 0:
            self.x = 0
            self.velocity = 0
        if self.x > 1500:
            self.x = 1500
            self.velocity = 0
        self.rect.x = int(self.x)
        self.slow_down = True
        self.check_collision()


pygame.init()
screen = pygame.display.set_mode((1600, 900))
player = Player()
pg = pygame.sprite.Group(player)
running = True
bricks = pygame.sprite.Group()
fps = 100
i = pygame.image.load('Images/YEP_Emote_Banner.png')
timer = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                Obstacle(*event.pos)
    t = timer.tick(fps)
    if pygame.key.get_pressed()[pygame.K_d]:
        player.move(1)
    if pygame.key.get_pressed()[pygame.K_a]:
        player.move(-1)
    bricks.update()
    attempt_obstacle_spawn(t)
    player.update(t / 1000)
    screen.fill('black')
    pg.draw(screen)
    bricks.draw(screen)
    pygame.display.flip()
