import pygame
import random
import os
from extramodule import SpriteSheet
from pygame import mixer
from Enemy import Enemy
#intialization
mixer.init()
pygame.init()
#fields
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
MAX_PLATFORM = 10
MAX_ENEMY = 5
WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255,0,100)
GRAVITY = 1
SCROLL_THRESH = 300
scroll = 0
bg_scroll = 0
game_over = False
score = 0
fade_counter = 0


if os.path.exists('score.txt'):
    with open ('score.txt', 'r') as file:
        high_score = int(file.read())
else:
    high_score = 0

font_small = pygame.font.SysFont('Lucida Sans', 20)
font_big = pygame.font.SysFont('Lucida Sans', 24)
#game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("platform jumping with asteroid falling")

#set game tick
clock = pygame.time.Clock()
FPS = 60

#load music
pygame.mixer.music.load('asset/bgmusic.mp3')
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play(-1, 0.0)

jump_fx = pygame.mixer.Sound('asset/jump_fx.mp3')
jump_fx.set_volume(0.5)

death_fx = pygame.mixer.Sound('asset/death_fx.mp3')
death_fx.set_volume(0.5)

#load image
player_image = pygame.image.load("asset/idle1.png").convert_alpha()
run_image = pygame.image.load('asset/Run_animation.png').convert_alpha()
run_image = pygame.transform.scale(run_image, (40, 45))
jump_image = pygame.image.load("asset/Jump_1.png")
jump_image = pygame.transform.scale(jump_image, (40,45))
bg = pygame.image.load("asset/bg.jpg").convert_alpha()
platform_image = pygame.image.load("asset/pad.png").convert_alpha()
bg = pygame.transform.scale(bg,(400,600))
asteroid = pygame.image.load("asset/asteroid1.png")
asteroid = pygame.transform.scale(asteroid,(10,10))
asteroid_sheet = SpriteSheet(asteroid)
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x,y))

def draw_panel():
    #pygame.draw.line(screen, WHITE, (0,30) , (SCREEN_WIDTH, 30), 2)
    draw_text('SCORE '  + str(score), font_small, WHITE, 0,0 )

def draw_bg(bg_scroll):
    screen.blit(bg, (0,0 + bg_scroll))
    screen.blit(bg, (0, -600 + bg_scroll))


#Player class
class Player:

    def __init__(self, x, y, player_image):

        self.image = pygame.transform.scale(player_image, (20, 45))
        self.width = 15
        self.height = 45
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.vel_x = 0
        self.flip = False
        self.on_ground = False

    def jump(self):
        if self.on_ground:  # Only jump if player is on the ground
            self.vel_y = -18  # Set the vertical velocity to make the player jump
            self.on_ground = False  # Update the on_ground flag
            jump_fx.play()

    def move(self):

        dx = 0
        dy = 0
        scroll = 0

        key = pygame.key.get_pressed()

        if key[pygame.K_a]:

            dx -= 8
            self.flip = True



        if key[pygame.K_d]:

            dx += 8
            self.flip = False



        if key[pygame.K_SPACE]:
            self.jump()
            self.image = jump_image



        self.vel_y += GRAVITY

        dy += self.vel_y

        if self.rect.left + dx < 0:
            dx = 0 - self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right


        for platform in platform_group:
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        #self.vel_y = -16
                        self.vel_y = 0
                        self.on_ground = True

        if self.rect.top <= SCROLL_THRESH:
            if self.vel_y < 0:
                scroll = -dy

        self.rect.x += dx
        self.rect.y += dy + scroll

        return scroll

    def draw(self, screen):
        if self.vel_x == 0 and self.vel_y == 0:
            self.image = pygame.transform.scale(player_image, (20, 45))
            screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        elif self.vel_x != 0 and self.vel_y == 0 and key[pygame.K_a] and key[pygame.K_d]:
            self.image = run_image
            screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        elif self.vel_y != 0:
            self.image = jump_image
            screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


        #pygame.draw.rect(screen,BLACK, self.rect, 1)


#class to create platform
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, platform_image, moving):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (width, 25))
        self.moving = moving
        self.move_counter = random.randint(0, 50)
        self.direction = random.choice([-1, 1])
        self.speed = random.randint(1,2)
        if score > 1500:
            self.speed = random.randint(1, 3)
        elif score > 5000:
            self.speed = random.randint(4, 5)
        elif score > 10000:
            self.speed = random.randint(5, 6)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self,scroll):
        if self.moving == True:
            self.move_counter += 1
            self.rect.x += self.direction * self.speed

        if self.move_counter >= 100 or self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction *= -1
            self.move_counter = 0

        self.rect.y += scroll

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

platform_group = pygame.sprite.Group()
asteroid_group = pygame.sprite.Group()

player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150, player_image)

platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT -120, 100, platform_image, False)
platform_group.add(platform)



#main game loop
run = True
while run:

    clock.tick(FPS)
    if game_over == False:
        scroll = player.move()

        bg_scroll += scroll
        if bg_scroll >= 768:
            bg_scroll = 0
        draw_bg(bg_scroll)

        platform_group.draw(screen)
        asteroid_group.draw(screen)
        player.draw(screen)

#death scenario
        if player.rect.top > SCREEN_HEIGHT:
            game_over = True
            death_fx.play()
        if pygame.sprite.spritecollide(player, asteroid_group, False):
            if pygame.sprite.spritecollide(player, asteroid_group, False, pygame.sprite.collide_mask):
                game_over = True
                death_fx.play()

#    pygame.draw.line(screen, WHITE, (0, SCROLL_THRESH), (SCREEN_WIDTH, SCROLL_THRESH))

        if len(platform_group) < MAX_PLATFORM:
            p_w = random.randint(50, 100)
            p_x = random.randint(0,SCREEN_WIDTH - p_w)
            p_y = platform.rect.y - random.randint(80, 120)
            p_type = random.randint(1, 2)
            if p_type == 1 and score > 500:
                p_moving = True
            else:
                p_moving = False
            platform = Platform(p_x, p_y, p_w, platform_image, p_moving)
            platform_group.add(platform)



        platform_group.update(scroll)

        if len(asteroid_group) < MAX_ENEMY:
            asteroid = Enemy(SCREEN_WIDTH, 10, asteroid_sheet, 3, score)
            asteroid_group.add(asteroid)

        asteroid_group.update(scroll, SCREEN_HEIGHT)

        if scroll > 0:
            score += scroll

        pygame.draw.line(screen, WHITE, (0,score - high_score + SCROLL_THRESH), (SCREEN_WIDTH, score - high_score + SCROLL_THRESH), 3)
        draw_text('HIGH_SCORE', font_small, WHITE, SCREEN_WIDTH -130, score - high_score + SCROLL_THRESH)
        draw_panel()
#game over
    else:
        if fade_counter < SCREEN_WIDTH:
            fade_counter += 5
            for y in range(0, 12, 2):
                pygame.draw.rect(screen, WHITE, (0, y * 50, fade_counter, SCREEN_HEIGHT / 12))
                pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - fade_counter, (y+1) * 50 , SCREEN_WIDTH, SCREEN_HEIGHT / 12))
        else:

            draw_text('GAME OVER! ', font_big, BLACK, 125, 200)
            draw_text('SCORE: ' + str(score), font_big, BLACK, 130, 250)
            draw_text('PRESS O TO PLAY AGAIN', font_big, BLACK, 40, 300)
            if score > high_score:
                high_score = score
                with open('score.txt', 'w') as file:
                    file.write(str(high_score))
            key = pygame.key.get_pressed()
            if key[pygame.K_o]:
                game_over = False
                score = 0
                scroll = 0
                fade_counter = 0
                player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
                asteroid_group.empty()
                platform_group.empty()
                platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 120, 100, platform_image, False)
                platform_group.add(platform)
#Quit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if score > high_score:
                high_score = score
                with open('score.txt', 'w') as file:
                    file.write(str(high_score))
            run = False

    pygame.display.update()

pygame.quit()

