import pygame


class Brick(pygame.sprite.Sprite):
    pass


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load('Images/YEP_Emote_Banner.png')
        self.image = pygame.transform.scale(self.image, (100, 200))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 700
        self.x = 0

    def move(self, direction=None, time=None):
        if (direction and time) is None:
            return None
        self.x += direction * time * 100
        if self.x < 0:
            self.x = 0
        if self.x > 1500:
            self.x = 1500
        self.rect.x = int(self.x)


pygame.init()
screen = pygame.display.set_mode((1600, 900))
player = Player()
pg = pygame.sprite.Group(player)
running = True
fps = 60
i = pygame.image.load('Images/YEP_Emote_Banner.png')
timer = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    t = timer.tick(fps)
    if pygame.key.get_pressed()[pygame.K_d]:
        player.move(1, t / 1000)
    if pygame.key.get_pressed()[pygame.K_a]:
        player.move(-1, t / 1000)
    screen.fill('black')
    pg.draw(screen)
    pygame.display.flip()
