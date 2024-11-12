import pygame
import sys


# Инициализация Pygame
pygame.init()

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


# Определяем размеры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('2D Game with Pygame')

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

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

while True:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Получаем нажатые клавиши
    keys = pygame.key.get_pressed()
    # Перемещение игрока
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

    # Отображаем всё на экране
    screen.fill(WHITE)  # Заполняем экран белым
    pygame.draw.rect(screen, GREEN, (player_x, player_y, player_width, player_height))  # Рисуем игрока

    # Рисуем препятствия
    for obstacle in obstacles:
        pygame.draw.rect(screen, BLACK, obstacle)

    draw_coin_counter()

    # Обновляем экран
    pygame.display.flip()

    # Ограничиваем количество кадров в секунду
    clock.tick(60)
