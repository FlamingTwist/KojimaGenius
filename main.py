import sys
from typing import Literal
from settings import *
from npc import *


# === ЛОГИКА ВЫТАЛКИВАНИЯ ===
def handle_collision(player_rect, box_rect, push_forse):
    """Выталкивает игрока, если он сталкивается с объектом"""
    if player_rect.colliderect(box_rect):
        # Вычисляем направление от коробки к игроку
        dx = player_rect.centerx - box_rect.centerx
        dy = player_rect.centery - box_rect.centery
        if dx != 0 or dy != 0:  # Если вектор не нулевой
            length = (dx**2 + dy**2)**0.5
            dx /= length  # Нормализация
            dy /= length  # Нормализация
            return dx * push_forse, dy * push_forse
    return 0, 0

# === ДОБАВЛЕНИЕ СЧЁТЧИКА МОНЕТОК ===
coin_count = 0
def draw_coin_counter():
    """Рисует счётчик монеток в правом верхнем углу"""
    coin_text = FONT.render(f"Кроны:{coin_count}", True, DIALOG_BLACK)
    screen.blit(coin_text, (SCREEN_WIDTH - coin_text.get_width() - 10, 10))

# === ЗОНЫ ВЗАИМОДЕЙСТВИЯ ===
INTERACTION_RADIUS = 100

def draw_interaction_zone(hitbox):
    """Рисует круг взаимодействия вокруг сундука"""
    pygm.draw.circle(screen, GREY, hitbox.center, INTERACTION_RADIUS, 1)

def check_interaction(player_rect, hitbox):
    """Проверяет, находится ли игрок в зоне взаимодействия с сундуком"""
    player_center = player_rect.center
    chest_center = hitbox.center
    distance = ((player_center[0] - chest_center[0])**2 + (player_center[1] - chest_center[1])**2)**0.5
    return distance <= INTERACTION_RADIUS

# === ДИАЛОГОВОЕ ОКНО ===
def draw_game_over(text):
    """Рисует окно GAME OVER"""
    # Размеры окна
    window_width = SCREEN_WIDTH - 100
    window_height = SCREEN_HEIGHT // 3
    window_x = (SCREEN_WIDTH - window_width) // 2
    window_y = (SCREEN_HEIGHT - window_height) // 2

    pygm.draw.rect(screen, WHITE, (window_x, window_y, window_width, window_height))
    pygm.draw.rect(screen, DIALOG_BLACK, (window_x+2, window_y+2, window_width-4, window_height-4), 3)

    # text = clicked_npc["game_over"]
    SMALL_FONT = pygm.font.Font(font_path, 16)

    # Текст GAME OVER
    text = text_to_lines(text, SMALL_FONT, window_width - 2*30)
    text.insert(0, " -- ИГРА ОКОНЧЕНА -- ")
    text = text[-5:] # Выводим только 5 последних строк
    
    for i in range(len(text)):
        text_surface = SMALL_FONT.render(text[i], True, DIALOG_BLACK)
        screen.blit(text_surface, (
            window_x + 30, 
            window_y + 22 + (SMALL_FONT.get_height() + 20) * i
        ))
    return None

# === ДИАЛОГОВОЕ ОКНО ===
def draw_dialogue_window(clicked_npc):
    """Рисует диалоговое окно с текстом и кнопками"""
    # Размеры окна
    dialog_width = SCREEN_WIDTH + 6
    dialog_height = 200
    dialog_x = (SCREEN_WIDTH - dialog_width) // 2
    dialog_y = SCREEN_HEIGHT - dialog_height

    # Координаты полотна для головы персонажа
    start_x, start_y = 450, 0       # Верхняя точка линии
    end_x, end_y = 600, SCREEN_HEIGHT  # Нижняя точка линии

    pygm.draw.polygon(screen, MIAMI_PURPLE, [
        (end_x, end_y),                 # Нижняя точка линии
        (SCREEN_WIDTH, SCREEN_HEIGHT),  # Нижний правый угол экрана
        (SCREEN_WIDTH, 0),              # Верхний правый угол экрана
        (start_x, start_y)              # Верхняя точка линии
    ])
    pygm.draw.line(screen, WHITE, (start_x+3, start_y), (end_x+3, end_y), 3)

    # Рисуем нижнее окно диалога и обводку
    pygm.draw.rect(screen, DIALOG_BLACK, (dialog_x, dialog_y, dialog_width, dialog_height))
    pygm.draw.rect(screen, WHITE, (dialog_x, dialog_y+3, dialog_width+2, dialog_height), 3)

    # Рисуем верхнее окно диалога и обводку
    pygm.draw.rect(screen, DIALOG_BLACK, (dialog_x, 0, dialog_width, dialog_height / 2))
    pygm.draw.rect(screen, WHITE, (dialog_x, -3, dialog_width+2, dialog_height / 2), 3)

    text, answer = get_dialog_text(clicked_npc) # Получаем текст диалога

    SMALL_FONT = pygm.font.Font(font_path, 16)

    # Имя NPC
    name = FONT.render(clicked_npc["name"], True, WHITE)
    screen.blit(name, (SCREEN_WIDTH - (70 + name.get_width()), 35))

    # Текст NPC
    text = text_to_lines(text, SMALL_FONT, SCREEN_WIDTH - 2*30)
    text = text[-5:] # Выводим только 5 последних строк
    
    for i in range(len(text)):
        text_surface = SMALL_FONT.render(text[i], True, WHITE)
        screen.blit(text_surface, (
            30, 
            dialog_y + 22 + (SMALL_FONT.get_height() + 20) * i
        ))

    # Настройки кнопок
    BUTTON_FILL_COLOR = DIALOG_BLACK  # Цвет заливки кнопок
    BUTTON_BORDER_COLOR = WHITE          # Цвет обводки кнопок
    BUTTON_TEXT_COLOR = WHITE            # Цвет текста кнопок
    BUTTON_X = SCREEN_WIDTH // 100   # Положение кнопок по X
    BUTTONS_Y = SCREEN_HEIGHT // 4   # Положение кнопок по X
    BUTTON_INTERVAL = 10                 # Отступ между кнопками
    BUTTON_WIDTH = 470                   # Ширина кнопок
    BUTTON_HEIGHT = 40                   # Высота кнопок
    # BUTTON_FONT = pygm.font.SysFont(None, 24)

    buttons: list[pygm.Rect] = []

    for i in range(len(answer)): # формирует 4 кнопки-ответа
        if (answer[i] == ""):
            continue

        button = pygm.Rect(
            BUTTON_X, 
            BUTTONS_Y + (BUTTON_HEIGHT + BUTTON_INTERVAL) * i, 
            BUTTON_WIDTH, 
            BUTTON_HEIGHT
        )
        pygm.draw.rect(screen, BUTTON_FILL_COLOR, button)  # Заливка
        pygm.draw.rect(screen, BUTTON_BORDER_COLOR, button, 2)  # Обводка
        button_text = SMALL_FONT.render(answer[i], True, BUTTON_TEXT_COLOR)
        screen.blit(button_text, button_text.get_rect(center=button.center))
        buttons.append(button)

    # return buttons[0], buttons[1], buttons[2], buttons[3]  # Возвращает области кнопок
    return buttons

# === ВРАЩЕНИЕ ГОЛОВЫ В ДИАЛОГЕ ===
def rotate_image(image, rect, angle):
    """
    Вращает изображение и возвращает его новую поверхность и прямоугольник.

    :param image: исходное изображение
    :param rect: прямоугольник изображения
    :param angle: угол вращения
    :return: повёрнутое изображение и обновлённый прямоугольник
    """
    rotated_image = pygm.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=rect.center)
    return rotated_image, new_rect

def blit_sort(x):
    return x[2]

""" 
 ###### ####### #####  ###### #######  
##         ##  ##   ## ##   ##   ##    
 #####     ##  ####### ######    ##    
     ##    ##  ##   ## ##  ##    ##    
######     ##  ##   ## ##   ##   ##    
"""


# Персонаж
player_width = 50
player_height = 50
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT // 2 - player_height // 2
PLAYER_SPEED = 8
flip_sprite = True

# Препятствия (rect) / NPC
NPC_PUSH_FORCE = 5
npcs = [
    [StrangerNPC, TrissNPC], # Левая сцена - индекс 0
    [CasinoOwnerNPC], # индекс 1
    [SuspiciousBankerNPC, ZoltanNPC] # Правая сцена - индекс 2
]

OBJ_PUSH_FORCE = 20
bridge_width = 100
lake_width = 100
lake_left_up = pygm.Rect(SCREEN_WIDTH - lake_width, 0, lake_width, (SCREEN_HEIGHT - bridge_width) // 2)
lake_left_down = pygm.Rect(SCREEN_WIDTH - lake_width, (SCREEN_HEIGHT + bridge_width) // 2, lake_width, (SCREEN_HEIGHT - bridge_width) // 2)
lake_right_up = pygm.Rect(0, 0, lake_width, (SCREEN_HEIGHT - bridge_width) // 2)
lake_right_down = pygm.Rect(0, (SCREEN_HEIGHT + bridge_width) // 2, lake_width, (SCREEN_HEIGHT - bridge_width) // 2)
wall_width = 80
wall_left = pygm.Rect(0, (SCREEN_HEIGHT - wall_width) // 2, SCREEN_WIDTH // 3, wall_width)
wall_right = pygm.Rect(SCREEN_WIDTH * 2 // 3, (SCREEN_HEIGHT - wall_width) // 2, SCREEN_WIDTH // 3, wall_width)

objs = [
    [wall_left],
    [lake_left_up, lake_left_down],
    [lake_right_up, lake_right_down, wall_right]
]

# Диалоги
angle = 0
MAX_ANGLE = 10
ANGLE_SPEED = 0.20
clockwise = True
dialog_open = False  # Флаг для открытия диалогового окна
clicked_npc = None  # Хранит NPC, который говорит
# TODO убрать масштабирование вручную, использовать 400% Aseprite

# Главный игровой цикл
clock = pygm.time.Clock()
game_state : Literal["exploration", "dialogue", "paused"] = "exploration"
current_scene = 1
mouse_down = False

while True:
    # Обработка событий
    for event in pygm.event.get():
        if event.type == pygm.QUIT:
            pygm.quit()
            sys.exit()

    # Получаем нажатые клавиши
    keys = pygm.key.get_pressed()

    # Перемещение игрока
    if game_state == "exploration":
        if keys[pygm.K_w] or keys[pygm.K_UP]:
            player_y -= PLAYER_SPEED
        if keys[pygm.K_s] or keys[pygm.K_DOWN]:
            player_y += PLAYER_SPEED
        if keys[pygm.K_a] or keys[pygm.K_LEFT]:
            player_x -= PLAYER_SPEED
            flip_sprite = False
        if keys[pygm.K_d] or keys[pygm.K_RIGHT]:
            player_x += PLAYER_SPEED
            flip_sprite = True

    if game_state == "exploration" or game_state == "paused":
        if keys[pygm.K_1]:
            pygm.quit()
            sys.exit()

    # Проверка на столкновение с границами экрана
    if player_x < 0:
        if (current_scene == 0):
            player_x = 0
        else:
            player_x = SCREEN_WIDTH - player_width
            current_scene -= 1
    if player_x + player_width > SCREEN_WIDTH:
        if (current_scene == 2):
            player_x = SCREEN_WIDTH - player_width
        else:
            player_x = 0
            current_scene += 1
    if player_y < 0:
        player_y = 0
    if player_y + player_height > SCREEN_HEIGHT:
        player_y = SCREEN_HEIGHT - player_height

    # Препятствия и их логика
    player_rect = pygm.Rect(player_x, player_y, player_width, player_height)

    for obj in objs[current_scene]:
        hitbox = obj
        # Проверка столкновений
        dx, dy = handle_collision(player_rect, hitbox, OBJ_PUSH_FORCE)
        # Применение выталкивания
        player_x += dx
        player_y += dy

    for npc in npcs[current_scene]:
        hitbox = npc["hitbox"]
        # Проверка столкновений
        dx, dy = handle_collision(player_rect, hitbox, NPC_PUSH_FORCE)
        # Применение выталкивания
        player_x += dx
        player_y += dy

        # Проверяем возможность взаимодействия
        if not dialog_open and game_state == "exploration" and check_interaction(player_rect, hitbox):
            if keys[pygm.K_e] or keys[pygm.K_9]:  # Взаимодействие на "E"
                print("Заход в NPC")
                game_state = "dialogue"
                dialog_open = True
                clicked_npc = npc

    # Отображаем всё на экране
    screen.fill(WHITE)  # Заполняем экран белым
    background = pygm.image.load("BWsprites/Background.png")
    background = pygm.transform.scale(background, (800, 600))
    screen.blit(background, (0, 0))

    blit_order = []

    if DEBUG:
        pygm.draw.rect(screen, MIAMI_PURPLE, player_rect)  # Рисуем игрока
    player = pygm.image.load("BWsprites/Chararacter.png")
    player = pygm.transform.scale(player, (100, 100))
    if flip_sprite == False:
        player = pygm.transform.flip(player, True, False)
        blit_order.append((player, player_x, player_y-50))
    else:
        blit_order.append((player, player_x-50, player_y-50))

    for obj in objs[current_scene]:
        hitbox = obj
        if DEBUG:
            pygm.draw.rect(screen, GREEN, hitbox)

    for npc in npcs[current_scene]:
        hitbox = npc["hitbox"]
        if DEBUG:
            pygm.draw.rect(screen, BLACK, hitbox)
            draw_interaction_zone(hitbox)
        npc_image = pygm.image.load("BWsprites/" + npc["sprite"])
        npc_image = pygm.transform.scale(npc_image, (100, 100))
        blit_order.append((npc_image, hitbox.centerx-50, hitbox.centery-75))
    
    # Сортировка персонажей по y и рендер
    blit_order.sort(key=blit_sort)
    
    # Но сначала тени -> создаем Surface с альфа-каналом
    shadow_surface = pygm.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygm.SRCALPHA) 
    for sprite in blit_order:
        shadow_hight = 24
        shadow_indent = 1
        transparency = 25
        pygm.draw.ellipse(shadow_surface, (0, 0, 0, transparency), (
            sprite[1] + shadow_indent, 
            sprite[2] + sprite[0].get_height() - shadow_hight // 2,
            sprite[0].get_width() - 2 * shadow_indent,
            shadow_hight)
        )
    screen.blit(shadow_surface, (0, 0))

    for sprite in blit_order:
        screen.blit(sprite[0], (sprite[1], sprite[2]))

    draw_coin_counter()

    # Отображение диалогового окна, если оно открыто
    if dialog_open:
        buttons = draw_dialogue_window(clicked_npc)

        # Логика контролируемого вращения головы
        # зависит от fps ¯\_(ツ)_/¯
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
        head = pygm.image.load("BWsprites/" + clicked_npc["head"])
        head = pygm.transform.scale(head, (380, 380))
        head_rect = head.get_rect(center=(SCREEN_WIDTH - 120, SCREEN_HEIGHT // 2 - 60))
        rotated_image, rotated_rect = rotate_image(head, head_rect, angle)
        screen.blit(rotated_image, rotated_rect)

        # Проверка кликов мыши
        if pygm.mouse.get_pressed()[0] and mouse_down == False: # ЛКМ нажата впервые
            mouse_pos = pygm.mouse.get_pos()
            mouse_down = True
            for i in range(len(buttons)):
                if buttons[i].collidepoint(mouse_pos):
                    dialog_open, coin_count = progress_questline(
                        clicked_npc,
                        i,
                        dialog_open,
                        coin_count)
                    if (dialog_open == False):
                        game_state = "exploration"
        elif not(pygm.mouse.get_pressed()[0]) and mouse_down == True: # ЛКМ отпущена
            mouse_down = False

    if (coin_count < 0) and game_state != "dialogue":
        game_state = "paused"
        draw_game_over(clicked_npc["game_over"])
    if (coin_count >= 300) and game_state != "dialogue":
        game_state = "paused"
        draw_game_over("Геральд смог накопить деньги на новые мечи и теперь может снова заниматься своим ремеслом")

    # Обновляем экран
    pygm.display.flip()

    # Ограничиваем количество кадров в секунду
    clock.tick(60)
