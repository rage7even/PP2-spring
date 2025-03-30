import pygame
import math

# Инициализация pygame
pygame.init()

# Настройки экрана
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Улучшенное приложение для рисования 🎨")

# Переменные состояния
drawing = False
last_pos = None
shape = "line"  # Доступные формы: 'line', 'rect', 'circle', 'eraser', 'square', 'right_triangle', 'equilateral_triangle', 'rhombus'
color = (0, 0, 0)  # Начальный цвет - черный
radius = 5  # Размер кисти/ластика

# Палитра цветов
colors = [
    (0, 0, 0),      # Черный
    (255, 0, 0),    # Красный
    (0, 255, 0),    # Зеленый
    (0, 0, 255),    # Синий
    (255, 255, 0),  # Желтый
    (255, 0, 255),  # Пурпурный
    (0, 255, 255),  # Бирюзовый
    (255, 255, 255) # Белый (ластик)
]

# Основной игровой цикл
running = True
screen.fill((255, 255, 255))  # Белый фон

def draw_right_triangle(surface, color, start_pos, end_pos, width=1):
    """Рисует прямоугольный треугольник"""
    points = [
        start_pos,
        (start_pos[0], end_pos[1]),
        end_pos
    ]
    pygame.draw.polygon(surface, color, points, width)

def draw_equilateral_triangle(surface, color, start_pos, end_pos, width=1):
    """Рисует равносторонний треугольник"""
    side_length = max(abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1]))
    height = int(side_length * math.sqrt(3) / 2)
    
    # Определяем направление рисования
    if end_pos[0] < start_pos[0]:
        side_length = -side_length
    if end_pos[1] < start_pos[1]:
        height = -height
    
    points = [
        start_pos,
        (start_pos[0] + side_length, start_pos[1]),
        (start_pos[0] + side_length // 2, start_pos[1] - height)
    ]
    pygame.draw.polygon(surface, color, points, width)

def draw_rhombus(surface, color, start_pos, end_pos, width=1):
    """Рисует ромб"""
    center_x = (start_pos[0] + end_pos[0]) // 2
    center_y = (start_pos[1] + end_pos[1]) // 2
    width = abs(end_pos[0] - start_pos[0]) // 2
    height = abs(end_pos[1] - start_pos[1]) // 2
    
    points = [
        (center_x, center_y - height),  # Верхняя точка
        (center_x + width, center_y),   # Правая точка
        (center_x, center_y + height),  # Нижняя точка
        (center_x - width, center_y)    # Левая точка
    ]
    pygame.draw.polygon(surface, color, points, width)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Нажатие кнопки мыши - начинаем рисование
        elif event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            last_pos = event.pos
            
            # Проверяем, выбрал ли пользователь цвет
            for i, col in enumerate(colors):
                rect = pygame.Rect(10 + i * 40, 10, 30, 30)
                if rect.collidepoint(event.pos):
                    color = col
                    if i == len(colors) - 1:  # Последний цвет (ластик)
                        shape = "eraser"
                    else:
                        shape = "line"
        
        # Отпускание кнопки мыши - заканчиваем рисование
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos
            
            # Рисуем фигуры, которые требуют завершающего действия
            if shape == "rect":
                width = end_pos[0] - last_pos[0]
                height = end_pos[1] - last_pos[1]
                pygame.draw.rect(screen, color, (last_pos[0], last_pos[1], width, height), radius)
            elif shape == "circle":
                dx = end_pos[0] - last_pos[0]
                dy = end_pos[1] - last_pos[1]
                radius_circle = int((dx**2 + dy**2)**0.5)
                pygame.draw.circle(screen, color, last_pos, radius_circle)
            elif shape == "square":
                size = max(abs(end_pos[0] - last_pos[0]), abs(end_pos[1] - last_pos[1]))
                if end_pos[0] < last_pos[0]:
                    x = last_pos[0] - size
                else:
                    x = last_pos[0]
                if end_pos[1] < last_pos[1]:
                    y = last_pos[1] - size
                else:
                    y = last_pos[1]
                pygame.draw.rect(screen, color, (x, y, size, size), radius)
            elif shape == "right_triangle":
                draw_right_triangle(screen, color, last_pos, end_pos, radius)
            elif shape == "equilateral_triangle":
                draw_equilateral_triangle(screen, color, last_pos, end_pos, radius)
            elif shape == "rhombus":
                draw_rhombus(screen, color, last_pos, end_pos, radius)
        
        # Нажатие клавиш для выбора инструментов
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:
                shape = "line"
            elif event.key == pygame.K_r:
                shape = "rect"
            elif event.key == pygame.K_c:
                shape = "circle"
            elif event.key == pygame.K_e:
                shape = "eraser"
                color = (255, 255, 255)  # Белый для ластика
            elif event.key == pygame.K_s:
                shape = "square"
            elif event.key == pygame.K_t:
                shape = "right_triangle"
            elif event.key == pygame.K_q:
                shape = "equilateral_triangle"
            elif event.key == pygame.K_h:
                shape = "rhombus"
        
        # Рисование (движение мыши)
        elif event.type == pygame.MOUSEMOTION and drawing:
            if shape == "line":
                pygame.draw.line(screen, color, last_pos, event.pos, radius)
                last_pos = event.pos
            elif shape == "eraser":
                pygame.draw.circle(screen, (255, 255, 255), event.pos, radius)
    
    # Рисуем палитру цветов
    for i, col in enumerate(colors):
        pygame.draw.rect(screen, col, (10 + i * 40, 10, 30, 30))
    
    # Отображаем текущий инструмент и подсказки
    font = pygame.font.SysFont(None, 24)
    tool_text = font.render(
        f"Инструмент: {shape.upper()} "
        "(L=Линия, R=Прямоуг., C=Круг, E=Ластик, "
        "S=Квадрат, T=Треуг.прям., Q=Треуг.равност., H=Ромб)", 
        True, (0, 0, 0))
    screen.blit(tool_text, (10, 50))
    
    pygame.display.flip()

pygame.quit()