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
        Obstacle(screen.get_width())


class Brick(pygame.sprite.Sprite):
    image = pygame.image.load('Images/BrickLongRound.png')

    def __init__(self, x, y, impassable=True, group:pygame.sprite.Group=None):
        if impassable:
            super(Brick, self).__init__(bricks)
        else:
            super(Brick, self).__init__(p_bricks)
            self.image = pygame.image.load('Images/BrickLongRound.png')
            self.image.blit(pygame.transform.scale(pygame.font.SysFont('comic sans', 20).render('YEP', True, pygame.color.Color('white')), (251, 124)), (0, 0))
        if group:
            group.add(self)
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
    def __init__(self, screen_width, right_bricks=1):
        bricks_ = screen_width // 251 + 1
        leftovers = screen_width % 251
        self.bricks = []
        self.group = pygame.sprite.Group()
        for brick in range(bricks_):
            if right_bricks > 0 and random.choice([0, 1]) == 1:
                print("YES")
                self.bricks.append(Brick(brick * 251 - leftovers // 2, -124, False, self.group))
                right_bricks -= 1
            else:
                if right_bricks > 0 and brick == bricks_ - 1:
                    print("YER")
                    self.bricks.append(Brick(brick * 251 - leftovers // 2, -124, False, group=self.group))
                else:
                    self.bricks.append(Brick(brick * 251 - leftovers // 2, -124, group=self.group))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load('Images/OMEGALUL.jpg')
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
            print('game over. You got {} points.'.format(int(score)))
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
font = pygame.font.SysFont('comic sans', 17)
score = 0
screen = pygame.display.set_mode((1600, 900))
player = Player()
pg = pygame.sprite.Group(player)
running = True
bricks = pygame.sprite.Group()
p_bricks = pygame.sprite.Group()
fps = 100
i = pygame.image.load('Images/OMEGALUL.jpg')
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
    p_bricks.update()
    score += t / 100
    attempt_obstacle_spawn(t)
    player.update(t / 1000)
    score_display = pygame.transform.scale(font.render(str(int(score)), 0, pygame.color.Color('white')),
                                           (67 * len(str(int(score))), 120))
    screen.fill('black')
    screen.blit(score_display, (screen.get_width() - score_display.get_width(), 0))
    pg.draw(screen)
    bricks.draw(screen)
    p_bricks.draw(screen)
    pygame.display.flip()
