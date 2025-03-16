import pygame
import os

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Music Player")
play_png = pygame.image.load(r"D:\PP2spring\py lab7\things\play.png").convert_alpha()
pause_png = pygame.image.load(r"D:\PP2spring\py lab7\things\pause.png").convert_alpha()
icon_rect = pause_png.get_rect(center=(400, 300))

music_folder = r"D:\PP2spring\py lab7\things"
playlist = [f for f in os.listdir(music_folder) if f.endswith(".mp3")]

if not playlist:
    print("NO music files found!")
    pygame.quit()
    exit()

currentTrack = 0
is_paused = False

def play_music():
    global is_paused
    pygame.mixer.music.load(os.path.join(music_folder,playlist[currentTrack]))
    pygame.mixer.music.play()
    is_paused = False
    print("Playing: ", playlist[currentTrack])

running = True
play_music()

while running:
    screen.fill((255, 255, 255))
    if is_paused:
        screen.blit(pause_png,icon_rect)
    else:
        screen.blit(play_png,(200,100))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                    is_paused = True
                else:
                    pygame.mixer.music.unpause()
                    is_paused = False
            elif event.key == pygame.K_SPACE:
                pygame.mixer.music.stop()
            elif event.key == pygame.K_RIGHT:
                currentTrack = (currentTrack+1) % len(playlist)
                play_music()
            elif event.key == pygame.K_LEFT:
                currentTrack = (currentTrack-1) % len(playlist)
                play_music()
