import pygame
import requests


def display_text(s: str):
    info = pygame.display.Info()
    screen = pygame.display.set_mode(
        (info.current_w, info.current_h), pygame.FULLSCREEN)
    screen_rect = screen.get_rect()
    font = pygame.font.Font(None, 45)
    clock = pygame.time.Clock()
    color = (000, 000, 000)
    txt = font.render(s, True, color)
    timer = 10
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

        timer -= 1
        # Update the text surface and color every 10 frames.
        if timer <= 0:
            timer = 10
            color = (000, 000, 000)
            txt = font.render(s, True, color)

        screen.fill((30, 30, 30))
        screen.blit(txt, txt.get_rect(center=screen_rect.center))

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    pygame.init()
    json = requests.get("http://localhost:3000/api/countdowns")
    display_text("This is my text!")
