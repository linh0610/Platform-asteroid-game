import pygame
import random
#intialization
pygame.init()
#constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
MAX_PLATFORM = 10
WHITE = (255, 255, 255)
GRAVITY = 1
SCROLL_THRESH = 300
scroll = 0
bg_scroll = 0
game_over = False
score = 0

font_small = pygame.font.SysFont('Lucida Sans', 20)
font_big = pygame.font.SysFont('Lucida Sans', 24)
#game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("jumping bullet hell")

clock = pygame.time.Clock()
FPS = 60

#load image
player_image = pygame.image.load("asset/idle1.png").convert_alpha()
bg = pygame.image.load("asset/bg.jpg").convert_alpha()
platform_image = pygame.image.load("asset/pad.png").convert_alpha()
bg = pygame.transform.scale(bg,(400,600))

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x,y))

def draw_bg(bg_scroll):
    screen.blit(bg, (0,0 + bg_scroll))
    screen.blit(bg, (0, -600 + bg_scroll))




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

    def move(self):

        dx = 0
        dy = 0
        scroll = 0

        key = pygame.key.get_pressed()

        if key[pygame.K_a]:
            dx -= 10
            self.flip = True
        if key[pygame.K_d]:
            dx += 10
            self.flip = False

        if key[pygame.K_SPACE]:
            self.jump()


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
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 1)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, platform_image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (width, 25))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self,scroll):

        self.rect.y += scroll
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

platform_group = pygame.sprite.Group()
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150, player_image)

platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT -120, 100, platform_image)
platform_group.add(platform)

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
        player.draw(screen)

        if player.rect.top > SCREEN_HEIGHT:
            game_over = True
#    pygame.draw.line(screen, WHITE, (0, SCROLL_THRESH), (SCREEN_WIDTH, SCROLL_THRESH))

        if len(platform_group) < MAX_PLATFORM:
            p_w = random.randint(50, 100)
            p_x = random.randint(0,SCREEN_WIDTH - p_w)
            p_y = platform.rect.y - random.randint(80, 120)
            platform = Platform(p_x, p_y, p_w, platform_image)
            platform_group.add(platform)



        platform_group.update(scroll)

    else:
        draw_text('GAME OVER! ', font_big, WHITE, 125, 200)
        draw_text('SCORE: ' + str(score), font_big, WHITE, 130, 250)
        draw_text('PRESS O TO PLAY AGAIN', font_big, WHITE, 40, 300)
        key = pygame.key.get_pressed()
        if key[pygame.K_o]:
            game_over = False
            score = 0
            scroll = 0
            player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
            platform_group.empty()
            platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 120, 100, platform_image)
            platform_group.add(platform)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()

