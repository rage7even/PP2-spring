import pygame
import random
import sys

# Инициализация pygame
pygame.init()

# Экран параметрлері
WIDTH, HEIGHT = 600, 400  # Ойын алаңының өлшемдері
CELL_SIZE = 20  # Ұяшық өлшемі (жыланның денесі мен тамақтың өлшемі)

# Түстер
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Терезені орнату
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Жылан сыныбы
class Snake:
    def __init__(self):
        self.body = [(100, 100), (90, 100), (80, 100)]  # Жыланның бастапқы ұзындығы
        self.direction = (CELL_SIZE, 0)  # Бастапқы қозғалыс бағыты

    def move(self):
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.body.insert(0, new_head)  # Басқа жаңа координат қосу
        self.body.pop()  # Соңғы элементті алып тастау

    def grow(self):
        self.body.append(self.body[-1])  # Жылан ұзарады

    def check_collision(self):
        head_x, head_y = self.body[0]
        # Шекарамен соқтығысу тексеру
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            return True
        # Өз денесімен соқтығысу тексеру
        if self.body[0] in self.body[1:]:
            return True
        return False

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

# Тамақ сыныбы
class Food:
    def __init__(self, snake_body):
        self.position = self.generate_new_position(snake_body)

    def generate_new_position(self, snake_body):
        while True:
            x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
            y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
            if (x, y) not in snake_body:  # Тамақ жылан денесінде пайда болмауы керек
                return (x, y)

    def draw(self, surface):
        pygame.draw.rect(surface, RED, (self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))

# Ойынды бастау
snake = Snake()
food = Food(snake.body)
clock = pygame.time.Clock()
score = 0
level = 1
speed = 10  # Бастапқы жылдамдық

# Ойын циклын бастау
running = True
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Басқару
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

    # Егер жылан тамақты жесе
    if snake.body[0] == food.position:
        score += 10  # Ұпай қосу
        snake.grow()
        food = Food(snake.body)

    # Деңгейді жоғарылату
    if score // 30 + 1 > level:
        level += 1
        speed += 2  # Жылдамдықты арттыру

    # Егер жылан қабырғаға немесе өз денесіне соғылса, ойын аяқталады
    if snake.check_collision():
        running = False

    # Ойын элементтерін салу
    snake.draw(screen)
    food.draw(screen)

    # Ұпай мен деңгей көрсету
    font = pygame.font.SysFont(None, 30)
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (WIDTH - 100, 10))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
sys.exit()