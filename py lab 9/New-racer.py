import pygame
from pygame.locals import * 
import random
import sys
import time

# Инициализация pygame
pygame.init()
FPS = 60  # Количество кадров в секунду
FramePerSec = pygame.time.Clock()  # Таймер для контроля FPS

# Определение цветов
colorBlack = pygame.Color(0, 0, 0)       # Черный
colorWhite = pygame.Color(255, 255, 255) # Белый
colorGrey = pygame.Color(128, 128, 128) # Серый
colorRed = pygame.Color(255, 0, 0)      # Красный
colorYellow = pygame.Color(255, 255, 0)  # Желтый
colorGreen = pygame.Color(0, 255, 0)    # Зеленый

# Настройка шрифтов
font = pygame.font.SysFont("Verdana", 60)        # Основной шрифт
font_small = pygame.font.SysFont("Verdana", 20)  # Мелкий шрифт
game_over = font.render("GAME OVER", True, colorBlack)  # Текст "Игра окончена"

# Загрузка фонового изображения
background = pygame.image.load(r"D:\PP2spring\py lab 8\things\AnimatedStreet.png")

# Игровые переменные
SPEED = 5                  # Начальная скорость врагов
SCORE = 0                  # Счет игрока
COINS_COLLECTED = 0        # Количество собранных монет
SPEED_INCREASE_THRESHOLD = 5  # Увеличивать скорость каждые 5 монет

# Настройка экрана
screen = pygame.display.set_mode((400, 600))
screen.fill(colorWhite)
pygame.display.set_caption("RACING")  # Заголовок окна

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Загрузка изображения машины игрока
        self.image = pygame.image.load(r"D:\PP2spring\py lab 8\things\Blue_Car.png").convert()
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)  # Начальная позиция игрока

    def update(self):
        # Обработка нажатий клавиш
        pressed_keys = pygame.key.get_pressed()
        
        # Движение вверх/вниз
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -2.5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 1)

        # Движение влево/вправо с проверкой границ экрана
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-2.5, 0)
        
        if self.rect.right < 600:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(2.5, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Загрузка изображения вражеской машины
        self.image = pygame.image.load(r"D:\PP2spring\py lab 8\things\Enemy.png").convert()
        self.rect = self.image.get_rect()
        # Случайная начальная позиция в верхней части экрана
        self.rect.center = (random.randint(40, 400-40), 0)

    def move(self):
        global SCORE
        # Движение врага вниз по экрану
        self.rect.move_ip(0, SPEED)
        
        # Если враг ушел за нижнюю границу - возрождаем его сверху
        if self.rect.bottom > 600:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, 400-40), 0)
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Загрузка и масштабирование изображения монеты
        self.image = pygame.image.load(r"D:\PP2spring\py lab 8\things\pixel-art-drawing-vector-graphics-royalty-free-2d-coin-sprite-20393662cdc2206bfd7df5f8307ede9b.png").convert()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        
        # Случайный вес (ценность) монеты от 1 до 5
        self.weight = random.randint(1, 5)
        
        # Окрашиваем монету в зависимости от ее ценности
        if self.weight == 1:
            self.image.fill(colorWhite, special_flags=pygame.BLEND_MULT)
        elif self.weight == 2:
            self.image.fill(colorYellow, special_flags=pygame.BLEND_MULT)
        elif self.weight >= 3:
            self.image.fill(colorGreen, special_flags=pygame.BLEND_MULT)
        
        self.spawn()  # Размещаем монету на экране
    
    def spawn(self):
        """Позиционирует монету в случайном месте на дороге"""
        self.rect.center = (random.randint(40, 400-60), random.randint(50, 600-200))
    
    def update(self):
        global SCORE, COINS_COLLECTED, SPEED
        
        # Проверка столкновения с игроком
        if pygame.sprite.collide_rect(self, P1):
            SCORE += self.weight  # Увеличиваем счет на ценность монеты
            COINS_COLLECTED += 1   # Увеличиваем счетчик собранных монет
            
            # Увеличиваем скорость врага каждые SPEED_INCREASE_THRESHOLD монет
            if COINS_COLLECTED % SPEED_INCREASE_THRESHOLD == 0:
                SPEED += 0.5
                print(f"Скорость увеличена! Текущая скорость: {SPEED}")
            
            self.spawn()  # Создаем новую монету

# Создание игровых объектов
P1 = Player()  # Игрок
E1 = Enemy()   # Враг
coin = Coin()  # Монета

# Создание групп спрайтов
enemies = pygame.sprite.Group()  # Группа врагов
enemies.add(E1)
all_sprites = pygame.sprite.Group()  # Все спрайты
coins = pygame.sprite.Group()        # Группа монет
coins.add(coin)
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(coin)

# Таймер для автоматического увеличения скорости
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)  # Увеличивать скорость каждую секунду

# Главный игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.1  # Небольшое автоматическое увеличение скорости
        if event.type == QUIT:
            running = False
            pygame.quit()
            sys.exit()
    
    # Обновление всех игровых объектов
    P1.update()
    E1.move()
    coin.update()

    # Отрисовка
    screen.fill(colorWhite)
    screen.blit(background, (0, 0))  # Рисуем фон
    
    # Отображение счета и количества монет
    scores = font_small.render(f"Счет: {SCORE}", True, colorBlack)
    coins_text = font_small.render(f"Монеты: {COINS_COLLECTED}", True, colorBlack)
    screen.blit(scores, (10, 10))
    screen.blit(coins_text, (10, 40))

    # Отрисовка всех спрайтов
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        entity.update()

    # Проверка столкновения игрока с врагами
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound(r"D:\PP2spring\py lab 8\things\crash.wav").play()  # Звук аварии
        time.sleep(0.5)
        screen.fill(colorRed)
        screen.blit(game_over, (30, 250))
        pygame.display.update()
        
        # Удаление всех спрайтов
        for entity in all_sprites:
            entity.kill()
            
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()  # Обновление экрана
    FramePerSec.tick(FPS)   # Поддержание заданного FPS