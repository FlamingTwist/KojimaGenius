import pygame as pygm

npc_width = 50
npc_height = 50
# npcs = [
#     pygm.Rect(200, 150, npc_width, npc_height),
#     pygm.Rect(400, 300, npc_width, npc_height),
#     pygm.Rect(600, 450, npc_width, npc_height)
# ]

def give_coin(game_stats):
    print("Получена монетка!")
    return game_stats[0], game_stats[1] + 1

def take_coin(game_stats):
    print("Потеряна монетка!")
    return game_stats[0], game_stats[1] - 1

def leave_dialog(game_stats):
    return False, game_stats[1]

GregNPC = {
    "name": "Greg",
    "sprite": "image.png",
    "hitbox": pygm.Rect(200, 150, npc_width, npc_height),
    "dialog_index": 0,
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
                {"action": leave_dialog, "next_dialog": None, "answer": "bye"}
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

def progress_questline(npc, selected_answer, dialog_open, coin_count) -> tuple[bool, int]:
    """Выполняет действие на основе выбранного ответа"""
    current_index = npc["dialog_index"]
    dialog = npc["dialogs"][current_index]
    answers = dialog["answers"]
    
    # Проверяем, что выбранный индекс корректен
    if not(0 <= selected_answer < len(answers)):
        raise ValueError("Выход за пределы ответов")

    selected_answer = answers[selected_answer]
    
    game_stats = (dialog_open, coin_count)
    action = selected_answer.get("action")
    if action:
        game_stats = action(game_stats) # Вызов соответсвующей функции

    # Обновляем индекс диалога
    next_dialog = selected_answer.get("next_dialog")
    if next_dialog is not None:
        npc["dialog_index"] = next_dialog

    # return dialog_open, coin_count
    return game_stats[0], game_stats[1]

