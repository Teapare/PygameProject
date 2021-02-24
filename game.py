import pygame
import sys
import random

FAKE_GRAVITY = 300  # px/sec
BRICK_SPAWN_INTERVAL = 4000  # ms
brick_spawn_counter = 3000  # ms
char_idle_animation = list(map(lambda x: pygame.image.load('Images/CharIdleAnimation.png').subsurface(*x),
                          [(0, 0, 646, 789), (803, 0, 657, 789), (0, 0, 646, 789)]))
char_running_animation = list(map(lambda x: pygame.image.load('Images/CharRunningAnimation.png').subsurface(*x),
                                  [(0, 0, 815, 789), (864, 0, 520, 789), (1379, 0, 691, 789)]))


def attempt_obstacle_spawn(t):
    global brick_spawn_counter
    brick_spawn_counter += t
    if brick_spawn_counter > BRICK_SPAWN_INTERVAL:
        brick_spawn_counter %= BRICK_SPAWN_INTERVAL
        Obstacle(screen.get_width())


class Brick(pygame.sprite.Sprite):
    image = pygame.image.load('Images/BrickLongRound.png')

    def __init__(self, x, y, impassable=True, group:pygame.sprite.Group = None):
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
    def __init__(self, screen_width, right_bricks=1, question=None, answers=None):
        bricks_ = screen_width // 251 + 1
        leftovers = screen_width % 251
        self.bricks = []
        self.group = pygame.sprite.Group()
        right = list(range(bricks_))
        right = [right.pop(random.randrange(len(right))) for i in range(right_bricks)]
        for brick in range(bricks_):
            if right_bricks > 0 and brick in right:
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
        self.image = char_idle_animation[0]
        self.idle_index = 0
        self.moving_index = 0
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 200 // self.image.get_height(), 200))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = screen.get_width() // 2 - self.rect.width // 2
        self.rect.y = 700
        self.x = self.rect.x
        self.orientation = 1
        self.velocity = 0
        self.v = 0
        self.slow_down = True
        self.idle_frame_counter = 0
        self.moving_frame_counter = 0

    def next_frame(self, time, distance):
        self.idle_frame_counter += time
        self.moving_frame_counter += distance
        if self.velocity == 0:
            self.moving_index = -1
            self.moving_frame_counter = 100
            if self.idle_frame_counter < 500:
                return None
            self.idle_frame_counter %= 500
            self.idle_index = (self.idle_index + 1) % 3
            self.image = char_idle_animation[self.idle_index]
        else:
            self.idle_index = -1
            self.idle_frame_counter = 500
            if self.moving_frame_counter < 150:
                return None
            self.moving_frame_counter %= 150
            self.moving_index = (self.moving_index + 1 ) % 3
            self.image = char_running_animation[self.moving_index]
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 200 // self.image.get_height(), 200))
        if self.orientation < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = 700

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
        for sprite in bricks.sprites():
            if pygame.sprite.collide_mask(self, sprite):
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
        if self.x > screen.get_width() - self.rect.width:
            self.x = screen.get_width() - self.rect.width
            self.velocity = 0
        self.rect.x = int(self.x)
        self.slow_down = True
        self.check_collision()
        self.next_frame(time * 1000, abs(time * self.velocity * self.orientation))


pygame.init()
font = pygame.font.SysFont('comic sans', 17)
screen = pygame.display.set_mode((1600, 900), pygame.FULLSCREEN)
player = Player()
fps = 100
bricks = pygame.sprite.Group()
p_bricks = pygame.sprite.Group()
i = pygame.image.load('Images/OMEGALULL.jpg')
pg = pygame.sprite.Group(player)
while True:
    score = 0
    running = True
    player.x = screen.get_width() // 2 - player.image.get_width() // 2
    timer = pygame.time.Clock()
    bricks.remove(*bricks.sprites())
    p_bricks.remove(*p_bricks.sprites())
    brick_spawn_counter = 3000
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Obstacle(screen.get_width())
        t = timer.tick(fps)
        if pygame.key.get_pressed()[pygame.K_d]:
            player.move(1)
        if pygame.key.get_pressed()[pygame.K_a]:
            player.move(-1)
        bricks.update()
        p_bricks.update()
        score += t / 100
        # attempt_obstacle_spawn(t)
        player.update(t / 1000)
        score_display = pygame.transform.scale(font.render(str(int(score)), 0, pygame.color.Color('white')),
                                               (67 * len(str(int(score))), 120))
        screen.fill('white')
        screen.blit(score_display, (screen.get_width() - score_display.get_width(), 0))
        pg.draw(screen)
        bricks.draw(screen)
        p_bricks.draw(screen)
        pygame.display.flip()
