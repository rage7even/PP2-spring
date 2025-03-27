import pygame
from pygame.locals import * 
import random
import sys
import time

pygame.init()
FPS = 60
FramePerSec = pygame.time.Clock()


colorBlack = pygame.Color(0,0,0)
colorWhite = pygame.Color(255,255,255)
colorGrey = pygame.Color(128,128,128)
colorREd = pygame.Color(255,0,0)
# Қаріптерді (шрифт) орнату
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20) # Кіші қаріп ( тиындарды көрсету)
game_over = font.render("GAME OVER", True,colorBlack) # "GAME OVER" текст жасау

background = pygame.image.load(r"D:\PP2spring\py lab 8\things\AnimatedStreet.png")

SPEED = 5
SCORE = 0

screen = pygame.display.set_mode((400, 600))
screen.fill(colorWhite)
pygame.display.set_caption("RACING")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"D:\PP2spring\py lab 8\things\Blue_Car.png").convert()
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)  # Ойыншының бастапқы орны

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0,-2.5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,1)


        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-2.5,0)
        
        if self.rect.right < 600:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(2.5,0)

    def draws(self, surface):
        surface.blit(self.image, self.rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"D:\PP2spring\py lab 8\things\Enemy.png").convert()
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(40,400-40),0)

    def moves(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.bottom > 600): #төменге түсіп кетсе, қайтадан жоғарғы жаққа шығару
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40,400-40),0)
        
    def draws(self,surface):
        surface.blit(self.image, self.rect)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"D:\PP2spring\py lab 8\things\pixel-art-drawing-vector-graphics-royalty-free-2d-coin-sprite-20393662cdc2206bfd7df5f8307ede9b.png").convert()
        self.image = pygame.transform.scale(self.image, (30,30))
        self.rect = self.image.get_rect()
        self.spawn()
    
    def spawn(self):
        self.rect.center = (random.randint(40,400-60), random.randint(50,600-200))
    
    def update(self):
        global SCORE
        if pygame.sprite.collide_rect(self,P1):
            SCORE += 5
            self.spawn()




P1 = Player()
E1 = Enemy()
coin = Coin()
# Топтарды жасау
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
coins = pygame.sprite.Group()
coins.add(coin)
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(coin)


INC_Speed = pygame.USEREVENT + 1
pygame.time.set_timer(INC_Speed,1000) # Әр 1 секунд сайын жылдамдықты арттыру

running = True
while running:
    for event in pygame.event.get():
        if event.type == INC_Speed:
            SPEED += 0.5
        if event.type == QUIT:
            running = False
            pygame.quit()
            sys.exit()
    

     # Барлық объектілерді жаңарту
    P1.update()
    E1.moves()
    coin.update()

    # Терезені тазалау және фонды қою
    screen.fill(colorWhite)
    screen.blit(background,(0,0))
    scores = font_small.render(str(SCORE), True, colorBlack)
    screen.blit(scores,(380,10))

    for entity in all_sprites:
        screen.blit(entity.image,entity.rect)
        entity.update()


    P1.draws(screen)
    E1.draws(screen)

     # Егер ойыншы қарсылас машинаға соғылса
    if pygame.sprite.spritecollideany(P1,enemies):
        pygame.mixer.Sound(r"D:\PP2spring\py lab 8\things\crash.wav").play()
        time.sleep(0.5)
        screen.fill(colorREd)
        screen.blit(game_over,(30,250))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()


    pygame.display.update()
    FramePerSec.tick(FPS)
