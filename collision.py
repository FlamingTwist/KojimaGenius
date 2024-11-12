import pygame

# === ЛОГИКА ВЫТАЛКИВАНИЯ ===
PUSH_FORCE = 3
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
# === END ЛОГИКА ВЫТАЛКИВАНИЯ ===


SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
BOX_WIDTH, BOX_HEIGHT = 100, 100
PLAYER_COLOR = (0, 128, 255)
BOX_COLOR = (255, 0, 0)
BG_COLOR = (0, 0, 0)
PLAYER_SPEED = 5

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D игра: игрок и коробка")
clock = pygame.time.Clock()

# Начальные позиции
player_x, player_y = 100, 100
box_x, box_y = 400, 300
# === END BOILERPLATE ===

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление игроком
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_y -= PLAYER_SPEED
    if keys[pygame.K_s]:
        player_y += PLAYER_SPEED
    if keys[pygame.K_a]:
        player_x -= PLAYER_SPEED
    if keys[pygame.K_d]:
        player_x += PLAYER_SPEED

    # Ограничение движения игрока
    player_x = max(0, min(SCREEN_WIDTH - PLAYER_WIDTH, player_x))
    player_y = max(0, min(SCREEN_HEIGHT - PLAYER_HEIGHT, player_y))

    # Проверка столкновений
    player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
    box_rect = pygame.Rect(box_x, box_y, BOX_WIDTH, BOX_HEIGHT)
    dx, dy = handle_collision(player_rect, box_rect)
    # Применение выталкивания
    player_x += dx
    player_y += dy

    # Отрисовка
    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, PLAYER_COLOR, player_rect)
    pygame.draw.rect(screen, BOX_COLOR, box_rect)
    pygame.display.flip()

    # Ограничение FPS
    clock.tick(60)

pygame.quit()