import pygame as pygm


# Отрисовка хитбоксов
DEBUG = False

# Цвета
WHITE = (255, 255, 255)
DIALOG_BLACK = (43, 43, 43)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GREY = (200, 200, 200)
MIAMI_PURPLE = (150,71,190)
MIAMI_RED = (248,87,67)

# Определяем размеры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Инициализация pygame
pygm.init()

font_path = "fonts/Press_Start_2P/PressStart2P-Regular.ttf"
# font_path = "fonts/Kablammo/static/Kablammo-Regular.ttf"
FONT = pygm.font.Font(font_path, 22)
# FONT = pygm.font.SysFont(None, 36)

screen = pygm.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygm.display.set_caption('2D Game with pygm')