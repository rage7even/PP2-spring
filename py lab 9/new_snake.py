import pygame
import random
import sys
import time

# Инициализация pygame
pygame.init()

# Параметры экрана
WIDTH, HEIGHT = 600, 400  # Размеры игрового поля
CELL_SIZE = 20  # Размер клетки (тело змейки и еды)

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Настройка окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Улучшенная Змейка")

class Snake:
    def __init__(self):
        self.body = [(100, 100), (90, 100), (80, 100)]  # Начальная длина змейки
        self.direction = (CELL_SIZE, 0)  # Начальное направление движения

    def move(self):
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.body.insert(0, new_head)  # Добавляем новую голову
        self.body.pop()  # Удаляем последний элемент

    def grow(self, amount=1):
        # Увеличиваем змейку на указанное количество сегментов
        for _ in range(amount):
            self.body.append(self.body[-1])

    def check_collision(self):
        head_x, head_y = self.body[0]
        # Проверка столкновения с границами
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            return True
        # Проверка столкновения с собственным телом
        if self.body[0] in self.body[1:]:
            return True
        return False

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

class Food:
    def __init__(self, snake_body):
        self.position = self.generate_new_position(snake_body)
        self.weight = random.randint(1, 3)  # Случайный вес еды (1-3)
        self.spawn_time = time.time()  # Время появления
        self.lifetime = random.uniform(5.0, 10.0)  # Время жизни (5-10 секунд)
        
    def generate_new_position(self, snake_body):
        while True:
            x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
            y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
            if (x, y) not in snake_body:  # Еда не должна появляться на змейке
                return (x, y)
    
    def is_expired(self):
        # Проверяем, истекло ли время жизни еды
        return time.time() - self.spawn_time > self.lifetime
    
    def draw(self, surface):
        # Рисуем еду разным цветом в зависимости от веса
        if self.weight == 1:
            color = RED
        elif self.weight == 2:
            color = YELLOW
        else:
            color = PURPLE
        
        pygame.draw.rect(surface, color, (self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))
        
        # Отображаем оставшееся время жизни (опционально)
        remaining_time = max(0, int(self.lifetime - (time.time() - self.spawn_time)))
        font = pygame.font.SysFont(None, 15)
        time_text = font.render(str(remaining_time), True, WHITE)
        screen.blit(time_text, (self.position[0] + 5, self.position[1] + 5))

# Инициализация игры
snake = Snake()
food = Food(snake.body)
clock = pygame.time.Clock()
score = 0
level = 1
speed = 10  # Начальная скорость
food_spawn_timer = 0
special_food_active = False

# Основной игровой цикл
running = True
while running:
    screen.fill(BLACK)
    
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Управление змейкой
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and snake.direction != (0, CELL_SIZE):
        snake.direction = (0, -CELL_SIZE)
    if keys[pygame.K_DOWN] and snake.direction != (0, -CELL_SIZE):
        snake.direction = (0, CELL_SIZE)
    if keys[pygame.K_LEFT] and snake.direction != (CELL_SIZE, 0):
        snake.direction = (-CELL_SIZE, 0)
    if keys[pygame.K_RIGHT] and snake.direction != (-CELL_SIZE, 0):
        snake.direction = (CELL_SIZE, 0)
    
    snake.move()
    
    # Проверка съедания еды
    if snake.body[0] == food.position:
        score += 10 * food.weight  # Увеличиваем счет с учетом веса еды
        snake.grow(food.weight)  # Увеличиваем змейку в зависимости от веса еды
        
        # Создаем новую еду
        food = Food(snake.body)
    
    # Проверка, не исчезла ли еда
    if food.is_expired():
        food = Food(snake.body)
    
    # Увеличение уровня и скорости
    if score // 30 + 1 > level:
        level += 1
        speed += 2
    
    # Проверка столкновений
    if snake.check_collision():
        running = False
    
    # Отрисовка игровых элементов
    snake.draw(screen)
    food.draw(screen)
    
    # Отображение информации
    font = pygame.font.SysFont(None, 30)
    score_text = font.render(f"Счет: {score}", True, WHITE)
    level_text = font.render(f"Уровень: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (WIDTH - 150, 10))
    
    # Подсказка по цветам еды
    hint_text = font.render("Красный=1, Желтый=2, Фиолет=3", True, WHITE)
    screen.blit(hint_text, (WIDTH//2 - 150, HEIGHT - 30))
    
    pygame.display.flip()
    clock.tick(speed)

# Завершение игры
pygame.quit()
sys.exit()