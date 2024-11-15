# npc_width = 50
# npc_height = 50
# npcs = [
#     pygm.Rect(200, 150, npc_width, npc_height),
#     pygm.Rect(400, 300, npc_width, npc_height),
#     pygm.Rect(600, 450, npc_width, npc_height)
# ]

# Возможные действия
GIVE_COIN = "coin"
TAKE_BERRY = "berry"

GregNPC = {
    "name": "Greg",
    "sprite": "image.png",
    "x": 200,
    "y": 150,
    "dialog_index": 0,
    "dialogs": [
        {#0
            # длинный текст будет выводиться частями в функции вывода диалога
            "text": "how are you?",
            # ответов не более 4
            "answers": [
                {"action": None, "next_dialog": 1, "answer": "normal"},
                {"action": None, "next_dialog": 1, "answer": "hungry"},
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
                {"action": GIVE_COIN, "next_dialog": None, "answer": "thank you"}
            ]
        },
        {#3
            "text": "Goodbye!",
            "answers": [
                {"action": None, "next_dialog": None, "answer": "bye"}
            ]
        }
    ]
}