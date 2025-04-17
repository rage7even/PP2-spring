import pygame
import random
import sys
import psycopg2

# === PostgreSQL connection ===
conn = psycopg2.connect(
    dbname="pydatabases", user="postgres", password="rage7even", host="localhost", port="5432"
)
cur = conn.cursor()

def get_or_create_user():
    username = input("Enter your username: ")
    cur.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    if user:
        user_id = user[0]
        cur.execute("SELECT level, score FROM user_score WHERE user_id = %s ORDER BY id DESC LIMIT 1", (user_id,))
        result = cur.fetchone()
        if result:
            return user_id, result[0], result[1]
        else:
            return user_id, 1, 0
    else:
        cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
        user_id = cur.fetchone()[0]
        conn.commit()
        return user_id, 1, 0

def save_score(user_id, level, score):
    cur.execute("INSERT INTO user_score (user_id, level, score) VALUES (%s, %s, %s)", (user_id, level, score))
    conn.commit()

# === Pygame init ===
pygame.init()
WIDTH, HEIGHT = 800, 800  # Updated resolution
CELL_SIZE = 20
WHITE, GREEN, RED, BLACK = (255,255,255), (0,255,0), (255,0,0), (0,0,0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake with PostgreSQL")
clock = pygame.time.Clock()

# === Wall definitions by level ===
def get_walls(level, snake_body):
    walls = []
    
    # Level 2: Horizontal walls at random positions, avoiding snake body
    if level >= 2:
        for _ in range(10):  # Randomly generate 10 horizontal walls
            x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
            y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
            if (x, y) not in snake_body:  # Avoid placing walls on snake
                walls.append((x, y))

    # Level 3: Vertical walls at random positions, avoiding snake body
    if level >= 3:
        for _ in range(10):  # Randomly generate 10 vertical walls
            x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
            y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
            if (x, y) not in snake_body:  # Avoid placing walls on snake
                walls.append((x, y))
                
    return walls

# === Snake class ===
class Snake:
    def __init__(self):
        self.body = [(100, 100), (80, 100), (60, 100)]
        self.direction = (CELL_SIZE, 0)

    def move(self):
        new_head = (self.body[0][0] + self.direction[0],
                    self.body[0][1] + self.direction[1])
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        self.body.append(self.body[-1])

    def check_collision(self, walls):
        head = self.body[0]
        if head in self.body[1:] or head in walls:
            return True
        x, y = head
        return x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, GREEN, (*segment, CELL_SIZE, CELL_SIZE))

# === Food class ===
class Food:
    def __init__(self, snake, walls):
        self.position = self.generate_position(snake, walls)

    def generate_position(self, snake, walls):
        while True:
            x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
            y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
            if (x, y) not in snake.body and (x, y) not in walls:
                return (x, y)

    def draw(self, surface):
        pygame.draw.rect(surface, RED, (*self.position, CELL_SIZE, CELL_SIZE))

# === Level selection menu ===
def select_level():
    selected_level = 1
    choosing = True
    font = pygame.font.SysFont(None, 40)
    while choosing:
        screen.fill(BLACK)
        title = font.render("Select Level (1-3) - Press Enter to Confirm", True, WHITE)
        choice = font.render(f"Current Level: {selected_level}", True, GREEN)
        screen.blit(title, (40, HEIGHT // 3))
        screen.blit(choice, (WIDTH // 3, HEIGHT // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_level = max(1, selected_level - 1)
                if event.key == pygame.K_RIGHT:
                    selected_level = min(3, selected_level + 1)
                if event.key == pygame.K_RETURN:
                    choosing = False
    return selected_level

# === Main game ===
def main():
    user_id, saved_level, score = get_or_create_user()
    level = select_level()
    speed = 10 + (level - 1) * 2
    snake = Snake()
    walls = get_walls(level, snake.body)
    food = Food(snake, walls)
    paused = False

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_score(user_id, level, score)
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                if event.key == pygame.K_ESCAPE:
                    save_score(user_id, level, score)
                    running = False

        if paused:
            pause_font = pygame.font.SysFont(None, 50)
            text = pause_font.render("Paused - Press P to Resume", True, WHITE)
            screen.blit(text, (WIDTH//2 - 200, HEIGHT//2))
            pygame.display.flip()
            clock.tick(5)
            continue

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

        if snake.body[0] == food.position:
            score += 10
            snake.grow()
            food = Food(snake, walls)

        if score // 50 + 1 > level:
            level += 1
            speed += 2
            walls = get_walls(level, snake.body)

        if snake.check_collision(walls):
            save_score(user_id, level, score)
            running = False

        snake.draw(screen)
        food.draw(screen)

        for wall in walls:
            pygame.draw.rect(screen, WHITE, (*wall, CELL_SIZE, CELL_SIZE))

        font = pygame.font.SysFont(None, 30)
        screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
        screen.blit(font.render(f"Level: {level}", True, WHITE), (WIDTH - 120, 10))

        pygame.display.flip()
        clock.tick(speed)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
