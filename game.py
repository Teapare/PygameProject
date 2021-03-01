import pygame
import sys
import random
from win32api import GetSystemMetrics

PLAYGROUND_SIZE = (800, 800)
BLACK = pygame.color.Color(0, 0, 0)
WHITE = pygame.color.Color(255, 255, 255)
FAKE_GRAVITY = 300  # px/sec
BRICK_SPAWN_INTERVAL = 4000  # ms

screen_size = (GetSystemMetrics(0), GetSystemMetrics(1))
playground_point_zero = ((screen_size[0] - PLAYGROUND_SIZE[0]) // 2, (screen_size[1] - PLAYGROUND_SIZE[1]) // 2)
brick_spawn_counter = 3000  # ms
char_idle_animation = list(map(lambda x: pygame.image.load('Images/CharIdleAnimation.png').subsurface(*x[:4]),
                               [(0, 0, 646, 789, 122, 200), (803, 0, 657, 789), (0, 0, 646, 789)]))
char_running_animation = list(map(lambda x: (pygame.image.load('Images/CharRunningAnimation.png').subsurface(*x[:4]),
                                             x[4], x[5]),
                                  [(0, 0, 815, 769, 815 * 150 // 769, 150), (864, 0, 520, 769, 520 * 150 // 769, 150),
                                   (1379, 0, 691, 769, 691 * 150 // 769, 150)]))
pause_btn = list(map(lambda im: pygame.transform.scale(im, (150, 150)),
                     (pygame.image.load('Images/pause.png'), pygame.image.load('Images/unpause.png'))))
pause_btn = {True: pause_btn[1], False: pause_btn[0]}


def pg_get_click(pos):
    x = pos[0]
    y = pos[1]
    if not (playground_point_zero[0] <= x <= playground_point_zero[0] + playground.get_width()):
        return False
    if not (playground_point_zero[1] <= y <= playground_point_zero[0] + playground.get_height()):
        return False
    return True


def pause_get_click(pos):
    x = pos[0]
    y = pos[1]
    if not (screen_size[0] - 200 <= x <= screen_size[0]):
        return False
    if not (screen_size[1] - 200 <= y <= screen_size[1]):
        return False
    return True


def difficulty(score):
    if score < 100:
        answer = random.randrange(2, 20)
        y = random.randrange(-answer, answer)
        x = answer - y
        question_ = "{} + {} =" if y >= 0 else "{} - {} ="
        question_ = question_.format(abs(x), abs(y))
        return playground, 1, 1, [str(answer)], [str(random.randrange(2, 20))], question_
    if 100 <= score <= 500:
        answer = random.randrange(2, 100)
        y = random.randrange(-answer + 1, answer)
        x = answer - y
        question_ = "{} + {} =" if y >= 0 else "{} - {} ="
        question_ = question_.format(abs(x), abs(y))
        return playground, 1, 1, [str(answer)], [str(random.randrange(2, 100))], question_
    if 500 < score < 1000:
        answer = random.randrange(100, 1000)
        y = random.randrange(-answer + 1, answer)
        x = answer - y
        question_ = "{} + {} =" if y >= 0 else "{} - {} ="
        question_ = question_.format(abs(x), abs(y))
        return playground, 1, 2, [str(answer)], \
               [str(random.randrange(answer - 300, min(answer + 300, 1000))) for i in range(2)], question_
    if score >= 1000:
        answer = random.randrange(100, 2000)
        y = random.randrange(-answer + 1, answer)
        x = answer - y
        question_ = "{} + {} =" if y >= 0 else "{} - {} ="
        question_ = question_.format(abs(x), abs(y))
        return playground, 1, 3, [str(answer)], \
               [str(random.randrange(answer - 200, min(answer + 200), 2000)) for i in range(3)], question_


def attempt_obstacle_spawn(t):
    global brick_spawn_counter
    brick_spawn_counter += t
    if brick_spawn_counter > BRICK_SPAWN_INTERVAL:
        brick_spawn_counter %= BRICK_SPAWN_INTERVAL
        Obstacle(*difficulty(score))


class Brick(pygame.sprite.Sprite):
    image = pygame.image.load('Images/BrickLongRound.png')

    def __init__(self, x, y, passable=False, p_text='', group: pygame.sprite.Group = None):
        if not passable:
            super(Brick, self).__init__(bricks)
            self.image = pygame.image.load('Images/BrickLongRound.png')
            if p_text:
                text = pygame.font.SysFont('comic sans', 200).render(p_text, True, pygame.color.Color('white'))
                text = pygame.transform.scale(text, (min(text.get_size(),
                                                         (self.image.get_width(),
                                                          text.get_height() * self.image.get_width()
                                                          // text.get_width()), key=lambda size: size[0])))
                # self.image.blit(pygame.transform.scale(text, (200, 124)), (0, 0))
                self.image.blit(text, ((self.image.get_width() - text.get_width()) // 2,
                                       (self.image.get_height() - text.get_height()) // 2))
        else:
            super(Brick, self).__init__(p_bricks)
            self.image = pygame.image.load('Images/BrickLongRound.png')
            text = pygame.font.SysFont('comic sans', 200).render(p_text, True, pygame.color.Color('white'))
            text = pygame.transform.scale(text, (min(text.get_size(),
                                                     (self.image.get_width(),
                                                      text.get_height() * self.image.get_width()
                                                      // text.get_width()), key=lambda size: size[0])))
            self.image.blit(text, ((self.image.get_width() - text.get_width()) // 2,
                                   (self.image.get_height() - text.get_height()) // 2))
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


# class Obstacle:
#     def __init__(self, screen_width, right_bricks=1, question=None, answers=None):
#         bricks_ = screen_width // 251 + 1
#         leftovers = screen_width % 251
#         self.bricks = []
#         self.group = pygame.sprite.Group()
#         right = list(range(bricks_))
#         right = [right.pop(random.randrange(len(right))) for i in range(right_bricks)]
#         for brick in range(bricks_):
#             if right_bricks > 0 and brick in right:
#                 print("YES")
#                 self.bricks.append(Brick(brick * 251 - leftovers // 2, -124, False, self.group))
#                 right_bricks -= 1
#             else:
#                 if right_bricks > 0 and brick == bricks_ - 1:
#                     print("YER")
#                     self.bricks.append(Brick(brick * 251 - leftovers // 2, -124, False, group=self.group))
#                 else:
#                     self.bricks.append(Brick(brick * 251 - leftovers // 2, -124, group=self.group))

class Obstacle:
    def __init__(self, surface: pygame.surface.Surface, correct: int = 0, incorrect: int = 0,
                 correct_answers=None, incorrect_answers: list = None, _question=''):
        if correct_answers is None:
            correct_answers = []
        if incorrect_answers is None:
            incorrect_answers = []
        bricks_amount = surface.get_width() // 200 + (1 if surface.get_width() % 200 != 0 else 0)
        correct_answers = [correct_answers.pop(random.randrange(len(correct_answers))) for i in range(correct)]
        self.bricks = random.sample(correct_answers, min(len(correct_answers), bricks_amount))
        self.bricks = [(elem, True) for elem in self.bricks]
        ia = random.sample(incorrect_answers, min(bricks_amount - len(self.bricks), len(incorrect_answers)))
        self.bricks += [(elem, False) for elem in ia]
        self.bricks += [('', False) for i in range(bricks_amount - len(self.bricks))]
        random.shuffle(self.bricks)
        _bricks = []
        for i, brick in enumerate(self.bricks):
            _bricks.append(Brick(i * 200 - (surface.get_width() % 200) / 2, -124, passable=brick[1], p_text=brick[0]))
        global question
        question = _question


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = char_idle_animation[0]
        self.idle_index = 0
        self.moving_index = 0
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 150 // self.image.get_height(), 150))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = playground_point_zero[0] + PLAYGROUND_SIZE[0] // 2 - self.rect.width // 2
        self.rect.y = 650
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
            self.image = pygame.transform.scale(self.image, (124, 160))
        else:
            self.idle_index = -1
            self.idle_frame_counter = 500
            if self.moving_frame_counter < 75:
                return None
            self.moving_frame_counter %= 75
            self.moving_index = (self.moving_index + 1) % 3
            # self.moving_index = 0
            self.image = char_running_animation[self.moving_index][0]
            self.image = pygame.transform.scale(self.image, char_running_animation[self.moving_index][1:])
        if self.orientation < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = playground.get_height() - self.rect.height

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
        if self.x > PLAYGROUND_SIZE[0] - 124:
            self.x = PLAYGROUND_SIZE[0] - 124
            self.velocity = 0
        self.rect.x = int(self.x)
        self.slow_down = True
        self.check_collision()
        self.next_frame(time * 1000, abs(time * self.velocity * self.orientation))


pygame.init()
font = pygame.font.SysFont('comic sans', 17)
screen = pygame.display.set_mode((1600, 900), pygame.FULLSCREEN)
playground = pygame.Surface(PLAYGROUND_SIZE)
player = Player()
fps = 100
bricks = pygame.sprite.Group()
p_bricks = pygame.sprite.Group()
pg = pygame.sprite.Group(player)
question = ''
while True:
    score = 0
    running = True
    paused = False
    player.x = playground_point_zero[0] + PLAYGROUND_SIZE[0] // 2 - player.rect.width // 2
    timer = pygame.time.Clock()
    bricks.remove(*bricks.sprites())
    p_bricks.remove(*p_bricks.sprites())
    brick_spawn_counter = 3000
    score_display = pygame.transform.scale(font.render(str(int(score)), False, WHITE),
                                           (67 * len(str(int(score))), 120))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                paused = not paused
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pg_get_click(event.pos):
                    Brick(event.pos[0] - playground_point_zero[0],
                          event.pos[1] - playground_point_zero[1])
                if pause_get_click(event.pos):
                    paused = not paused
        t = timer.tick(fps)
        screen.fill(BLACK)
        if not paused:
            if pygame.key.get_pressed()[pygame.K_d]:
                player.move(1)
            if pygame.key.get_pressed()[pygame.K_a]:
                player.move(-1)
            bricks.update()
            p_bricks.update()
            score += t / 100
            attempt_obstacle_spawn(t)
            player.update(t / 1000)
            score_display = pygame.transform.scale(font.render(str(int(score)), False, WHITE),
                                                   (67 * len(str(int(score))), 120))
            question_display = pygame.transform.scale(font.render(question, False, WHITE),
                                                      (min(67 * len(question), playground_point_zero[0]), 120))
            screen.blit(question_display, (0, 0))
        playground.fill(WHITE)
        screen.blit(score_display, (screen.get_width() - score_display.get_width(), 0))
        pg.draw(playground)
        if not paused:
            bricks.draw(playground)
            p_bricks.draw(playground)
        screen.blit(pause_btn[paused], (screen_size[0] - 200, screen_size[1] - 200))
        screen.blit(playground, playground_point_zero)
        pygame.display.flip()
