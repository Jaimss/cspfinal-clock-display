import pygame
import requests
from datetime import datetime
import time

pygame.init()

SIZE = WIDTH, HEIGHT = (1920, 1080)
FPS = 30
screen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 150)


def blit_text(surface, text, pos, font, color=pygame.Color('#efefef')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


def format(eventname, td):
    seconds = td.seconds
    days = td.days
    if (days < 0):
        return str(f'{eventname.capitalize()} is finally here!')
    hours = seconds // (60 * 60)
    seconds %= (60 * 60)
    minutes = seconds // 60
    seconds %= 60
    return str(f'{eventname.capitalize()} is in:\n{days} days...\n{hours} hours...\n{minutes} minutes...\n{seconds} seconds...')


def getTd(data, eventname):
    return data[eventname] - datetime.now()


def updatedata():
    json = requests.get("http://localhost:3000/api/countdowns").json()
    data = {}
    for countdown in json:
        date = datetime.strptime(
            f"{countdown['month']}/{countdown['day']}/{countdown['year']} {countdown['hour']}:{countdown['minute']}", "%m/%d/%Y %H:%M")
        data[countdown['name']] = date
    return data

data = updatedata()

x = 0
y = 0
while True:
    x += 1
    dt = clock.tick(FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    if (x % 60 == 0):
        data = updatedata()

    try:
        eventname = list(data.keys())[y]
    except IndexError:
        y = 0
        eventname = list(data.keys())[y]
    if (x % 10 == 0):
        y+=1


    screen.fill(pygame.Color('#121212'))
    blit_text(screen, format(eventname, getTd(data, eventname)), (40, 40), font)
    pygame.display.update()
    time.sleep(1)