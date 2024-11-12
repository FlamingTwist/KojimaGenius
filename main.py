import pygame
import sys
from typing import Literal


# Инициализация Pygame
pygame.init()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GREY = (200, 200, 200)

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
    dialog_width = 400
    dialog_height = 200
    dialog_x = (SCREEN_WIDTH - dialog_width) // 2
    dialog_y = SCREEN_HEIGHT - dialog_height - 10

    # Рисуем окно диалога
    pygame.draw.rect(screen, (240, 240, 240), (dialog_x, dialog_y, dialog_width, dialog_height))  # Белое окно
    pygame.draw.rect(screen, BLACK, (dialog_x, dialog_y, dialog_width, dialog_height), 3)  # Обводка

    # Текст "Вы открыли сундук"
    text = font.render("Вы открыли сундук", True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, dialog_y + 40))
    screen.blit(text, text_rect)

    # Кнопка "Выйти из сундука"
    exit_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20, 200, 40)
    pygame.draw.rect(screen, (200, 200, 200), exit_button_rect)  # Серый цвет
    pygame.draw.rect(screen, BLACK, exit_button_rect, 2)  # Обводка
    exit_text = font.render("Выйти из сундука", True, BLACK)
    screen.blit(exit_text, exit_text.get_rect(center=exit_button_rect.center))

    # Кнопка "Понюхать сундук и выйти"
    sniff_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 40, 200, 40)
    pygame.draw.rect(screen, (200, 200, 200), sniff_button_rect)  # Серый цвет
    pygame.draw.rect(screen, BLACK, sniff_button_rect, 2)  # Обводка
    sniff_text = font.render("Понюхать сундук и выйти", True, BLACK)
    screen.blit(sniff_text, sniff_text.get_rect(center=sniff_button_rect.center))

    return exit_button_rect, sniff_button_rect  # Возвращаем области кнопок


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

# Главный игровой цикл
clock = pygame.time.Clock()
dialog_open = False  # Флаг для открытия диалогового окна
clicked_chest = None  # Хранит сундук, который открылся
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
                print("Заход в сундук")
                game_state = "dialogue"
                dialog_open = True
                clicked_chest = obstacle

    # Отображаем всё на экране
    screen.fill(WHITE)  # Заполняем экран белым
    pygame.draw.rect(screen, GREEN, (player_x, player_y, player_width, player_height))  # Рисуем игрока

    # TODO понять почему у нас два цикла obstacles раздельно
    for obstacle in obstacles:
        pygame.draw.rect(screen, BLACK, obstacle)
        draw_interaction_zone(obstacle)

    # Отображение диалогового окна, если оно открыто
    if dialog_open:
        exit_button, sniff_button = draw_dialogue_window()

        # Проверка кликов мыши
        if pygame.mouse.get_pressed()[0]:  # ЛКМ нажата
            mouse_pos = pygame.mouse.get_pos()
            if exit_button.collidepoint(mouse_pos):
                dialog_open = False  # Закрыть диалог
                game_state = "exploration"
            elif sniff_button.collidepoint(mouse_pos):
                print("Вы понюхали сундук и вышли!")  # Логика нюханья сундука
                dialog_open = False  # Закрыть диалог
                game_state = "exploration"

    draw_coin_counter()

    # Обновляем экран
    pygame.display.flip()

    # Ограничиваем количество кадров в секунду
    clock.tick(60)
