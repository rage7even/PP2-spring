import pygame
import datetime

pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Mickey Clock")
background_image = pygame.image.load(r"D:\PP2spring\py lab7\things\clock.png").convert_alpha()
right_hand = pygame.image.load(r"D:\PP2spring\py lab7\things\sec_hand.png").convert_alpha()
left_hand = pygame.image.load(r"D:\PP2spring\py lab7\things\min_hand.png").convert_alpha()

right_hand_rect = right_hand.get_rect(center=(400, 300))
left_hand_rect = left_hand.get_rect(center=(400, 300))
clock_face_rect = background_image.get_rect(center=(400, 300))

'''icon = pygame.image.load("py lab7\things")
pygame.display.set_icon(icon)'''

running = True
while running:
    now = datetime.datetime.now()
    minutes = now.minute
    seconds = now.second
    minutes_angle = -(minutes * 4 + seconds * 0.1)
    seconds_angle = -(seconds * 7 + 21)
    rotated_right = pygame.transform.rotate(right_hand, minutes_angle)
    rotated_right_rect = rotated_right.get_rect(center=right_hand_rect.center)

    rotated_left = pygame.transform.rotate(left_hand, seconds_angle)
    rotated_left_rect = rotated_left.get_rect(center=left_hand_rect.center)


    screen.fill((255, 255, 255))
    screen.blit(background_image,clock_face_rect)
    screen.blit(rotated_right,rotated_right_rect)
    screen.blit(rotated_left,rotated_left_rect)

    pygame.display.flip()
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
