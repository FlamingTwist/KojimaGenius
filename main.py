import pygame
import sys
from typing import Literal


# Инициализация Pygame
pygame.init()

# Цвета
WHITE = (255, 255, 255)
DIALOG_BLACK = (43, 43, 43)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GREY = (200, 200, 200)
MIAMI_PURPLE = (150,71,190)
MIAMI_RED = (248,87,67)

# === ЛОГИКА ВЫТАЛКИВАНИЯ ===
PUSH_FORCE = 5
def handle_collision(player_rect, box_rect):
    """
    Выталкивает игрока, если он сталкивается с коробкой.
    """
    if player_rect.colliderect(box_rect):
        # Вычисляем направление от коробки к игроку
        dx = player_rect.centerx - box_rect.centerx
        dy = player_rect.centery - box_rect.centery
        if dx != 0 or dy != 0:  # Если вектор не нулевой
            length = (dx**2 + dy**2)**0.5
            dx /= length  # Нормализация
            dy /= length  # Нормализация
            return dx * PUSH_FORCE, dy * PUSH_FORCE
    return 0, 0

# === ДОБАВЛЕНИЕ СЧЁТЧИКА МОНЕТОК ===
font = pygame.font.SysFont(None, 36)
coin_count = 0
def draw_coin_counter():
    """Рисует счётчик монеток в правом верхнем углу."""
    coin_text = font.render(f"Coins: {coin_count}", True, BLACK)
    screen.blit(coin_text, (SCREEN_WIDTH - coin_text.get_width() - 10, 10))

# === ЗОНЫ ВЗАИМОДЕЙСТВИЯ ===
INTERACTION_RADIUS = 100

def draw_interaction_zone(chest):
    """Рисует круг взаимодействия вокруг сундука."""
    pygame.draw.circle(screen, GREY, chest.center, INTERACTION_RADIUS, 1)

def check_interaction(player_rect, chest):
    """Проверяет, находится ли игрок в зоне взаимодействия с сундуком."""
    player_center = player_rect.center
    chest_center = chest.center
    distance = ((player_center[0] - chest_center[0])**2 + (player_center[1] - chest_center[1])**2)**0.5
    return distance <= INTERACTION_RADIUS

# === ДИАЛОГОВОЕ ОКНО ===
def draw_dialogue_window():
    """Рисует диалоговое окно с текстом и кнопками."""
    # Размеры окна
    dialog_width = SCREEN_WIDTH + 6
    dialog_height = 200
    dialog_x = (SCREEN_WIDTH - dialog_width) // 2
    dialog_y = SCREEN_HEIGHT - dialog_height

    # Координаты полотна для головы персонажа
    start_x, start_y = 450, 0       # Верхняя точка линии
    end_x, end_y = 600, SCREEN_HEIGHT  # Нижняя точка линии

    pygame.draw.polygon(screen, MIAMI_PURPLE, [
        (end_x, end_y),                 # Нижняя точка линии
        (SCREEN_WIDTH, SCREEN_HEIGHT),  # Нижний правый угол экрана
        (SCREEN_WIDTH, 0),              # Верхний правый угол экрана
        (start_x, start_y)              # Верхняя точка линии
    ])
    pygame.draw.line(screen, WHITE, (start_x+3, start_y), (end_x+3, end_y), 3)

    # Рисуем нижнее окно диалога
    pygame.draw.rect(screen, DIALOG_BLACK, (dialog_x, dialog_y, dialog_width, dialog_height))
    pygame.draw.rect(screen, WHITE, (dialog_x, dialog_y+3, dialog_width+2, dialog_height), 3)  # Обводка

    # Рисуем верхнее окно диалога
    pygame.draw.rect(screen, DIALOG_BLACK, (dialog_x, 0, dialog_width, dialog_height / 2))
    pygame.draw.rect(screen, WHITE, (dialog_x, -3, dialog_width+2, dialog_height / 2), 3)  # Обводка

    # Текст "Вы открыли сундук"
    text = font.render("DO YOU LIKE HURTING OTHER PEOPLE?", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 3, dialog_y + 40))
    screen.blit(text, text_rect)

    # Настройки кнопок
    BUTTON_FILL_COLOR = DIALOG_BLACK  # Цвет заливки кнопок
    BUTTON_BORDER_COLOR = WHITE          # Цвет обводки кнопок
    BUTTON_TEXT_COLOR = WHITE            # Цвет текста кнопок
    BUTTON_X = SCREEN_WIDTH // 7   # Положение кнопок по X
    BUTTONS_Y = SCREEN_HEIGHT // 4   # Положение кнопок по X
    BUTTON_INTERVAL = 10                 # Отступ между кнопками
    BUTTON_WIDTH = 280                   # Ширина кнопок
    BUTTON_HEIGHT = 40                   # Высота кнопок
    BUTTON_FONT = pygame.font.SysFont(None, 24)

    # Кнопка "Выйти из сундука"
    exit_button_rect = pygame.Rect(
        BUTTON_X, BUTTONS_Y + (BUTTON_HEIGHT + BUTTON_INTERVAL) * 2, BUTTON_WIDTH, BUTTON_HEIGHT
    )
    pygame.draw.rect(screen, BUTTON_FILL_COLOR, exit_button_rect)  # Заливка
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, exit_button_rect, 2)  # Обводка
    exit_text = BUTTON_FONT.render("Ох, я ошибся NPC", True, BUTTON_TEXT_COLOR)
    screen.blit(exit_text, exit_text.get_rect(center=exit_button_rect.center))

    # Кнопка "Понюхать сундук и выйти"
    coin_button_rect = pygame.Rect(
        BUTTON_X, BUTTONS_Y + (BUTTON_HEIGHT + BUTTON_INTERVAL) * 3, BUTTON_WIDTH, BUTTON_HEIGHT
    )
    pygame.draw.rect(screen, BUTTON_FILL_COLOR, coin_button_rect)  # Заливка
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, coin_button_rect, 2)  # Обводка
    coin_text = BUTTON_FONT.render("Получить монетку", True, BUTTON_TEXT_COLOR)
    screen.blit(coin_text, coin_text.get_rect(center=coin_button_rect.center))

    return exit_button_rect, coin_button_rect  # Возвращаем области кнопок

# === ВРАЩЕНИЕ ГОЛОВЫ В ДИАЛОГЕ ===
def rotate_image(image, rect, angle):
    """
    Вращает изображение и возвращает его новую поверхность и прямоугольник.

    :param image: исходное изображение
    :param rect: прямоугольник изображения
    :param angle: угол вращения
    :return: вращённое изображение и обновлённый прямоугольник
    """
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=rect.center)
    return rotated_image, new_rect

# Определяем размеры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('2D Game with Pygame')

# Персонаж
player_width = 50
player_height = 50
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT // 2 - player_height // 2
PLAYER_SPEED = 5

# Препятствия
obstacle_width = 100
obstacle_height = 100
obstacles = [
    pygame.Rect(200, 150, obstacle_width, obstacle_height),
    pygame.Rect(400, 300, obstacle_width, obstacle_height),
    pygame.Rect(600, 450, obstacle_width, obstacle_height)
]

# Диалоги
angle = 0
MAX_ANGLE = 10
ANGLE_SPEED = 0.20
clockwise = True
dialog_open = False  # Флаг для открытия диалогового окна
clicked_chest = None  # Хранит сундук, который открылся
# head = pygame.image.load('image.png')  # Замените на путь к вашему изображению
# head = pygame.transform.scale(image, (200, 200))  # Масштабируем изображение
square_size = 180
square_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)  # Прозрачная поверхность
square_surface.fill(MIAMI_RED)
image_rect = square_surface.get_rect(center=(SCREEN_WIDTH - 150, SCREEN_HEIGHT // 2 - 50))

# Главный игровой цикл
clock = pygame.time.Clock()
game_state : Literal["exploration", "dialogue", "paused"] = "exploration"

while True:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Получаем нажатые клавиши
    keys = pygame.key.get_pressed()

    # Перемещение игрока
    if game_state == "exploration":
        if keys[pygame.K_w]:  # Вверх
            player_y -= 10
        if keys[pygame.K_s]:  # Вниз
            player_y += 10
        if keys[pygame.K_a]:  # Влево
            player_x -= 10
        if keys[pygame.K_d]:  # Вправо
            player_x += 10

    # Проверка на столкновение с границами экрана
    if player_x < 0:
        player_x = 0
    if player_x + player_width > SCREEN_WIDTH:
        player_x = SCREEN_WIDTH - player_width
    if player_y < 0:
        player_y = 0
    if player_y + player_height > SCREEN_HEIGHT:
        player_y = SCREEN_HEIGHT - player_height

    # Препятствия и их логика
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for obstacle in obstacles:
        # Проверка столкновений
        dx, dy = handle_collision(player_rect, obstacle)
        # Применение выталкивания
        player_x += dx
        player_y += dy

        # Проверяем возможность взаимодействия
        if not dialog_open and check_interaction(player_rect, obstacle):
            if keys[pygame.K_e]:  # Открытие сундука на "E"
                print("Заход в NPC")
                game_state = "dialogue"
                dialog_open = True
                clicked_chest = obstacle

    # Отображаем всё на экране
    screen.fill(WHITE)  # Заполняем экран белым
    pygame.draw.rect(screen, GREEN, (player_x, player_y, player_width, player_height))  # Рисуем игрока

    draw_coin_counter()

    # TODO понять почему у нас два цикла obstacles раздельно
    for obstacle in obstacles:
        pygame.draw.rect(screen, BLACK, obstacle)
        draw_interaction_zone(obstacle)

    # Отображение диалогового окна, если оно открыто
    if dialog_open:
        exit_button, sniff_button = draw_dialogue_window()

        # Логика контролируемого вращения головы
        # TODO зависит от fps ¯\_(ツ)_/¯
        if angle <= MAX_ANGLE and clockwise:
            angle += ANGLE_SPEED
        elif angle > MAX_ANGLE:
            clockwise = not(clockwise)
            angle = MAX_ANGLE - ANGLE_SPEED
        elif angle >= -MAX_ANGLE and not(clockwise):
            angle -= ANGLE_SPEED
        else:
            clockwise = not(clockwise)
            angle = -MAX_ANGLE + ANGLE_SPEED

        # Вращение изображения
        rotated_image, rotated_rect = rotate_image(square_surface, image_rect, angle)
        
        # Отображение вращённого изображения
        screen.blit(rotated_image, rotated_rect)

        # Проверка кликов мыши
        if pygame.mouse.get_pressed()[0]:  # ЛКМ нажата
            mouse_pos = pygame.mouse.get_pos()
            if exit_button.collidepoint(mouse_pos):
                dialog_open = False  # Закрыть диалог
                game_state = "exploration"
            elif sniff_button.collidepoint(mouse_pos):
                print("Вы получили монетку и вышли!")  # Логика нюханья сундука
                coin_count += 1
                dialog_open = False  # Закрыть диалог
                game_state = "exploration"

    # Обновляем экран
    pygame.display.flip()

    # Ограничиваем количество кадров в секунду
    clock.tick(60)
