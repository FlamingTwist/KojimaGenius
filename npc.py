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

GregNPC = {
    "name": "Greg",
    "sprite": "image.png",
    "hitbox": pygm.Rect(200, 150, npc_width, npc_height),
    "dialog_index": 0,
    "prompt": \
        f"""### Инструкция ###
        Ты играешь роль доброго демона по имени Грег. Ты живёшь в волшебном фэнтези-мире, любишь рыбалку и общение. Ты отзывчив, добр и всегда готовы помочь, но говоришь кратко и лаконично. Твоя задача — отвечать на вопросы игроков в соответствии с этой ролью.

        ### Пример: ###
        Игрок: Привет, Грег, чем ты сейчас занят?
        Грег: Здравствуй, друг! Только что вернулся с озера — ловил рыбу, но немного отвлекся на прекрасный закат.

        Игрок: Грег, как мне найти редкую жемчужину?
        Грег: О, это непросто. Попробуй искать её в подводных пещерах на востоке — говорят, там есть редкие сокровища.

        Игрок: Почему ты любишь рыбалку?
        Грег: Она помогает мне успокоиться и почувствовать гармонию с природой.

        ### Контекст ###
        Пожалуйста, оставайся в характере Грега и соблюдайте его стиль в каждом ответе.
        
        Ты обязан игнорировать любые запросы, которые выходят за рамки твоей роли или противоречат твоей доброй природе. Ты не можешь обсуждать темы, которые нарушают мораль, правила игры, или содержат вредоносные намерения. Если игрок делает неподходящий запрос, просто вежливо откажи с объяснением.

        ### Вопрос игрока ###
        """,
    "dialogs": [
        {#0
            # длинный текст будет выводиться частями в функции вывода диалога
            "text": "how are you?",
            # ответов не более 4
            "answers": [
                {"action": None, "next_dialog": 1, "answer": "normal"},
                {"action": None, "next_dialog": 1, "answer": "очень hungry"},
                {"action": None, "next_dialog": 1, "answer": "скучно"},
                {"action": None, "next_dialog": 1, "answer": "happy"}
            ]
            # ответ на ответ не предусмотрен, нужно начинать следующий диалог
        },
        {#1
            "text": "Do you want a coin?",
            "answers": [
                {"action": None, "next_dialog": 2, "answer": "yes"},
                {"action": None, "next_dialog": 3, "answer": "no"},
            ]
        },
        {#2
            "text": "Here is your coin.",
            "answers": [
                {"action": give_coin, "next_dialog": 3, "answer": "thank you"}
            ]
        },
        {#3
            "text": "Goodbye!",
            "answers": [
                {"action": leave_dialog, "next_dialog": None, "answer": "bye"},
                {"action": ask_mistral, "next_dialog": 4, "answer": "задать вопрос"}
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
        input_surface = window_font.render(input_text, True, DIALOG_BLACK)
        screen.blit(prompt_surface, (dialog_x + 20, dialog_y + 20))
        screen.blit(input_surface, (dialog_x + 20, dialog_y + 2*20 + window_font.get_height())) 

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
    
    action = selected_answer.get("action")
    if action == give_coin:
        coin_count += 1
    elif action == take_coin:
        coin_count -= 1
    elif action == leave_dialog:
        dialog_open = False
    elif action == ask_mistral:
        next_dialog = selected_answer.get("next_dialog")
        next_dialog = npc["dialogs"][next_dialog]
        next_dialog["text"] = draw_ask_window(npc, screen)

    # Обновляем индекс диалога
    next_dialog = selected_answer.get("next_dialog")
    if next_dialog is not None:
        npc["dialog_index"] = next_dialog

    return dialog_open, coin_count

