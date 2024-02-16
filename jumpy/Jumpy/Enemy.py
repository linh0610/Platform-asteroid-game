import pygame
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, SCREEN_WIDTH, y, sprite_sheet, scale, score):
        pygame.sprite.Sprite.__init__(self)
        self.x = random.randint(0,400)
        self.dy = random.randint(1,3)
        if score > 1500:
            self.dy = random.randint(3,4)
        elif score > 5000:
            self.dy = random.randint(6,7)
        elif score > 10000:
            self.dy = random.randint(10,16)


        image = sprite_sheet.get_image(0, 32,32 ,scale, (0,0,0))
        image.set_colorkey((0,0,0))
        self.image = image
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = y

    def update(self, scroll, SCREEN_HEIGHT):
        self.rect.y += scroll

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
        self.rect.y += self.dy
