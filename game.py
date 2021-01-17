import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load('Images/YEP_Emote_Banner.png')
        self.image = pygame.transform.scale(self.image, (100, 200))
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 1400

    def move(self, direction=None, time=None):
        if (direction and time) is None:
            return None
        self.rect.x += direction * time
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > 1500:
            self.rect.x = 1500


pygame.init()
screen = pygame.display.set_mode((1600, 900))

