import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    
    radius = 15
    x, y = 0, 0
    mode = 'blue'
    drawing_mode = 'freehand'  # 'freehand', 'rectangle', 'circle', 'eraser'
    points = []
    start_pos = None
    colors = {'blue': (0, 0, 255), 'red': (255, 0, 0), 'green': (0, 255, 0), 'eraser': (0, 0, 0)}
    
    while True:
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return
                
                if event.key == pygame.K_r:
                    mode = 'red'
                elif event.key == pygame.K_g:
                    mode = 'green'
                elif event.key == pygame.K_b:
                    mode = 'blue'
                elif event.key == pygame.K_e:
                    drawing_mode = 'eraser'
                elif event.key == pygame.K_t:
                    drawing_mode = 'rectangle'
                elif event.key == pygame.K_y:
                    drawing_mode = 'circle'
                elif event.key == pygame.K_f:
                    drawing_mode = 'freehand'
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if drawing_mode in ['rectangle', 'circle']:
                        start_pos = event.pos
                    else:
                        points.append(event.pos)
                elif event.button == 3:  # Right click
                    radius = max(1, radius - 1)
            
            if event.type == pygame.MOUSEMOTION:
                if drawing_mode == 'freehand' and pygame.mouse.get_pressed()[0]:
                    points.append(event.pos)
                    points = points[-256:]
                elif drawing_mode == 'eraser' and pygame.mouse.get_pressed()[0]:
                    pygame.draw.circle(screen, (0, 0, 0), event.pos, radius)
            
            if event.type == pygame.MOUSEBUTTONUP:
                if drawing_mode in ['rectangle', 'circle'] and start_pos:
                    end_pos = event.pos
                    if drawing_mode == 'rectangle':
                        pygame.draw.rect(screen, colors[mode], pygame.Rect(start_pos, (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])))
                    elif drawing_mode == 'circle':
                        center = ((start_pos[0] + end_pos[0]) // 2, (start_pos[1] + end_pos[1]) // 2)
                        radius = max(abs(end_pos[0] - start_pos[0]) // 2, abs(end_pos[1] - start_pos[1]) // 2)
                        pygame.draw.circle(screen, colors[mode], center, radius)
                    start_pos = None
        
        screen.fill((0, 0, 0))
        
        for i in range(len(points) - 1):
            pygame.draw.line(screen, colors[mode], points[i], points[i + 1], radius)
        
        pygame.display.flip()
        clock.tick(60)

main()