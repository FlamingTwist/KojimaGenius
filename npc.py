from settings import *
import os
from dotenv import load_dotenv
import requests

npc_width = 50
npc_height = 50
# npcs = [
#     pygm.Rect(200, 150, npc_width, npc_height),
#     pygm.Rect(400, 300, npc_width, npc_height),
#     pygm.Rect(600, 450, npc_width, npc_height)
# ]

def give_coin():
    print("Получена монетка!")

def take_coin():
    print("Потеряна монетка!")

def game_over():
    print("Потеряна 1000 монеток!")

def leave_dialog():
    pass

def ask_mistral(npc, user_prompt: str) -> str:
    # TODO узнать про новые модели
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
    try:
        # Загрузить переменные из .env файла
        load_dotenv()
        API_TOKEN = os.getenv("API_TOKEN") 
        
        headers = {"Authorization": f"Bearer {API_TOKEN}"}

        prompt = npc["prompt"] + f" '{user_prompt}'."

        full_prompt = f"<s>[INST] {prompt} [/INST]"
        payload = {
            "inputs": full_prompt,
            "parameters": {"max_new_tokens": 1024}
        }
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()[0]['generated_text'][len(full_prompt):]
    except:
        return ""

CasinoOwnerNPC = {
    "name": "Владелец казино",
    "sprite": "Casino.png",
    "head": "Head_Casino.png",
    "hitbox": pygm.Rect(300, 200, npc_width, npc_height),
    "dialog_index": 0,
    "game_over": "Геральд проиграл все деньги и попал в долговую яму",
    "dialogs": [
        {#0
            "text": "Молодой человек, не желаете ли преумножить свой капитал?",
            "answers": [
                {"action": None, "next_dialog": 1, "answer": "С большим удовольствием"},
                {"action": leave_dialog, "next_dialog": None, "answer": "Нет, спасибо"}
            ]
        },
        {#1
            "text": "Предлагаю Вам сыграть в моём казино 1Х Спирт. Я уверен, вы урвете большой куш.",
            "answers": [
                {"action": None, "next_dialog": 2, "answer": "Но у меня нет денег..."},
                {"action": leave_dialog, "next_dialog": None, "answer": "Холера, до свидания"}
            ]
        },
        {#2
            "text": "Не беспокойтесь, вы можете взять у нашего казино кредит в 200% годовых. Ну что, сыграете?",
            "answers": [
                {"action": game_over, "next_dialog": 3, "answer": "Вот это разговор!"},
                {"action": leave_dialog, "next_dialog": None, "answer": "Что-то мне это не нравится"}
            ]
        },
        {#3
            "text": "Отлично!",
            "answers": [
                {"action": leave_dialog, "next_dialog": None, "answer": "..."}
            ]
        }
    ]
}
SuspiciousBankerNPC = {
    "name": "Подозрительный банкир",
    "sprite": "Ded.png",
    "head": "Head_Ded.png",
    "hitbox": pygm.Rect(300, 200, npc_width, npc_height),
    "dialog_index": 0,
    "game_over": "Геральд не смог отдать деньги, поэтому попал в рабство на чайные плантации",
    "dialogs": [
        {#0
            "text": "Добро пожаловать ко мне в банк! Чего пожелаете?",
            "answers": [
                {"action": None, "next_dialog": 1, "answer": "Мне нужно много денег"},
                {"action": leave_dialog, "next_dialog": None, "answer": "У вас штукатурка отвалилась"}
            ]
        },
        {#1
            "text": "Я могу предоставить вам ипотеку на вашу жизнь и ваших детей. Также кредит, который, если Вы не выплатите через 2 дня, будет повышаться втрое. Что вас интересует?",
            "answers": [
                {"action": None, "next_dialog": 2, "answer": "Деньги"},
                {"action": leave_dialog, "next_dialog": None, "answer": "Ничего, до свидания"}
            ]
        },
        {#2
            "text": "Отлично, оформим все. Подпишите вот эту стопку бумаг.",
            "answers": [
                {"action": game_over, "next_dialog": 3, "answer": "[Подписать]"},
                {"action": None, "next_dialog": 4, "answer": "[Словить прилив осознанности]"}
            ]
        },
        {#3
            "text": "Хороший выбор!",
            "answers": [
                {"action": leave_dialog, "next_dialog": None, "answer": "..."}
            ]
        },
        {#4
            "text": "Вы куда?",
            "answers": [
                {"action": leave_dialog, "next_dialog": 5, "answer": "Всего доброго..."}
            ]
        },
        {#5
            "text": "...",
            "answers": [
                {"action": leave_dialog, "next_dialog": None, "answer": "..."}
            ]
        }
    ]
}
ZoltanNPC = {
    "name": "Золтан",
    "sprite": "Zoltan.png",
    "head": "Head_Zoltan.png",
    "hitbox": pygm.Rect(400, 200, npc_width, npc_height),
    "dialog_index": 0,
    "dialogs": [
        {#0
            "text": "Привет, дружище, какими судьбами?",
            "answers": [
                {"action": None, "next_dialog": 1, "answer": "Можно одолжить денег?"},
                {"action": leave_dialog, "next_dialog": None, "answer": "Забудь..."}
            ]
        },
        {#1
            "text": "Ты меня столько раз выручал. Конечно, можно. Я как раз припрятал мешочек на черный день!",
            "answers": [
                {"action": give_coin, "next_dialog": 2, "answer": "[Взять деньги]"},
                {"action": give_coin, "next_dialog": 2, "answer": "Спасибо"}
            ]
        },
        {#2
            "text": "До скорой встречи!",
            "answers": [
                {"action": leave_dialog, "next_dialog": 3, "answer": "..."}
            ]
        },
        {#3
            "text": "Что-то хотел спросить?",
            "answers": [
                {"action": ask_mistral, "next_dialog": 4, "answer": "Ага!"},
                {"action": leave_dialog, "next_dialog": None, "answer": "Неа..."}
            ]
        },
        {#4
            "text": "Этот текст будет затёрт ответом от gpt4o-mini",
            "answers": [
                {"action": leave_dialog, "next_dialog": 3, "answer": "..."}
            ]
        }
    ]
}
StrangerNPC = {
    "name": "Незнакомец в капюшоне",
    "sprite": "Man.png",
    "head": "Head_Man.png",
    "hitbox": pygm.Rect(100, 200, npc_width, npc_height),
    "dialog_index": 0,
    "game_over": "Мужчина оказался служителем правопорядка под прикрытием. Геральда арестовали",
    "dialogs": [
        {#0
            "text": "Хочешь подзаработать?",
            "answers": [
                {"action": None, "next_dialog": 1, "answer": "Слушаю"},
                {"action": leave_dialog, "next_dialog": None, "answer": "Я тебе не знаю"}
            ]
        },
        {#1
            "text": "Работа простая, нужно всего лишь спрятать парочку пакетиков чая за деревьями. Интересует?",
            "answers": [
                {"action": game_over, "next_dialog": 2, "answer": "Звучит просто,давай пакетики"},
                {"action": leave_dialog, "next_dialog": None, "answer": "Воздержусь от таких работ"}
            ]
        },
        {#2
            "text": "О, друг, пойдём!",
            "answers": [
                {"action": leave_dialog, "next_dialog": None, "answer": "Холера!"}
            ]
        }
    ]
}
TrissNPC = {
    "name": "Трисс",
    "sprite": "Triss.png",
    "head": "Head_Triss.png",
    "hitbox": pygm.Rect(400, 200, npc_width, npc_height),
    "dialog_index": 0,
    "dialogs": [
        {#0
            "text": "Геральд, рада тебя видеть!",
            "answers": [
                {"action": None, "next_dialog": 1, "answer": "Есть работенка?"},
                {"action": leave_dialog, "next_dialog": None, "answer": "Будь здорова"}
            ]
        },
        {#1
            "text": "Только грязная. Нужно выгнать крыс со склада. Платят неплохо.",
            "answers": [
                {"action": None, "next_dialog": 2, "answer": "[Начать работу] (+200 крон)"},
                {"action": leave_dialog, "next_dialog": None, "answer": "Не, не хочу"}
            ]
        },
        {#2
            "text": "...",
            "answers": [
                {"action": give_coin, "next_dialog": 3, "answer": "[Работать]"}
            ]
        },
        {#3
            "text": "...",
            "answers": [
                {"action": give_coin, "next_dialog": 4, "answer": "[Ещё работать]"}
            ]
        },
        {#4
            "text": "Отлично поработал. Вот оплата",
            "answers": [
                {"action": leave_dialog, "next_dialog": None, "answer": "[Взять деньги]"},
                {"action": leave_dialog, "next_dialog": None, "answer": "Спасибо!"}
            ]
        }
    ]
}

def get_dialog_text(npc) -> tuple[str, list[str]]:
    """Текущий текст NPC и список вариантов ответов для диалогового окна"""
    current_index = npc["dialog_index"]
    if not(0 <= current_index < len(npc["dialogs"])):
        raise ValueError("Выход за пределы диалогов")
    
    dialog = npc["dialogs"][current_index]
    
    # Получаем текст и список текстов ответов (не больше 4)
    text: str = dialog["text"]
    answers: list[str] = [answer["answer"] for answer in dialog["answers"]]
    
    return text, answers

def text_to_lines(text: str, font: pygm.font.Font, allowed_width: int) -> list[str]:
    current_line = ""
    lines = []

    # Разбиваем текст на строки
    for char in text:
        test_line = f"{current_line}{char}"
        input_surface = font.render(test_line, True, BLACK)
        if input_surface.get_width() <= allowed_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = char

    # Добавляем последнюю строку
    if current_line:
        lines.append(current_line.strip())
    
    return lines if lines != [] else [""]

def draw_ask_window(npc, screen: pygm.Surface) -> str:
    """Отображает окно с вводом текста поверх основной игры"""
    prompt_text = "Введите вопрос:"
    input_text = "" # Вводимый текст
    window_font = pygm.font.Font(font_path, 16)
    
    overlay = pygm.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)  # Прозрачность затемнения
    overlay.fill(DIALOG_BLACK)
    screen.blit(overlay, (0, 0))

    dialog_x = SCREEN_WIDTH // 8
    dialog_y = SCREEN_HEIGHT // 3
    dialog_width = SCREEN_WIDTH - 2 * dialog_x
    dialog_height = SCREEN_HEIGHT - 2 * dialog_y

    while True:
        for event in pygm.event.get():
            if event.type == pygm.QUIT:
                return "..."

            if event.type == pygm.KEYDOWN:
                if event.key == pygm.K_RETURN: # Enter
                    return ask_mistral(npc, input_text)

                elif event.key == pygm.K_BACKSPACE: # Backspace
                    input_text = input_text[:-1]

                else:
                    # Добавляем символ в текст, если это не служебная клавиша
                    input_text += event.unicode

        pygm.draw.rect(screen, WHITE, (dialog_x, dialog_y, dialog_width, dialog_height))
        pygm.draw.rect(screen, DIALOG_BLACK, (dialog_x + 2, dialog_y + 2, dialog_width - 4, dialog_height - 4), 2)

        prompt_surface = window_font.render(prompt_text, True, DIALOG_BLACK)
        screen.blit(prompt_surface, (dialog_x + 20, dialog_y + 20))

        text_lines = text_to_lines(input_text, window_font, dialog_width - 2*20)
        text_lines = text_lines[-4:] # Выводим только 4 последних строки
        
        for i in range(len(text_lines)):
            input_surface = window_font.render(text_lines[i], True, DIALOG_BLACK)
            screen.blit(input_surface, (
                dialog_x + 20, 
                dialog_y + 20 + (window_font.get_height() + 20) * (i + 1)
            )) 
            
        pygm.display.flip()


def progress_questline(npc, selected_answer, dialog_open, coin_count) -> tuple[bool, int]:
    """Выполняет действие на основе выбранного ответа"""
    current_index = npc["dialog_index"]
    dialog = npc["dialogs"][current_index]
    answers = dialog["answers"]
    
    # Проверяем, что выбранный индекс корректен
    if not(0 <= selected_answer < len(answers)):
        raise ValueError("Выход за пределы ответов")

    selected_answer = answers[selected_answer]
    
    action = selected_answer["action"]
    if action == give_coin:
        give_coin()
        coin_count += 100
    elif action == take_coin:
        take_coin()
        coin_count -= 100
    elif action == game_over:
        game_over()
        coin_count -= 1000
    elif action == leave_dialog:
        leave_dialog()
        dialog_open = False
    elif action == ask_mistral:
        next_dialog = selected_answer["next_dialog"]
        next_dialog = npc["dialogs"][next_dialog]
        next_dialog["text"] = draw_ask_window(npc, screen)

    # Обновляем индекс диалога
    next_dialog = selected_answer["next_dialog"]
    if next_dialog is not None:
        npc["dialog_index"] = next_dialog

    return dialog_open, coin_count

