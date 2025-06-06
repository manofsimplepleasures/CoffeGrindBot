"""
Клавиатуры для Telegram бота
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Создает основную клавиатуру бота."""
    keyboard = [
        [KeyboardButton("⚙️ Настройки"), KeyboardButton("📊 Рекомендации")],
        [KeyboardButton("❓ Помощь"), KeyboardButton("📝 О боте")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_settings_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру настроек кофемолки."""
    keyboard = [
        [
            InlineKeyboardButton("Крупность помола", callback_data="grind_size"),
            InlineKeyboardButton("Время помола", callback_data="grind_time")
        ],
        [
            InlineKeyboardButton("Тип кофе", callback_data="coffee_type"),
            InlineKeyboardButton("Метод заваривания", callback_data="brew_method")
        ],
        [
            InlineKeyboardButton("Сохранить настройки", callback_data="save_settings")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_grind_size_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру выбора крупности помола."""
    keyboard = [
        [
            InlineKeyboardButton("Очень мелкий", callback_data="grind_very_fine"),
            InlineKeyboardButton("Мелкий", callback_data="grind_fine")
        ],
        [
            InlineKeyboardButton("Средний", callback_data="grind_medium"),
            InlineKeyboardButton("Крупный", callback_data="grind_coarse")
        ],
        [
            InlineKeyboardButton("Очень крупный", callback_data="grind_very_coarse")
        ],
        [
            InlineKeyboardButton("« Назад", callback_data="back_to_settings")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_coffee_type_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру выбора типа кофе."""
    keyboard = [
        [
            InlineKeyboardButton("Арабика", callback_data="coffee_arabica"),
            InlineKeyboardButton("Робуста", callback_data="coffee_robusta")
        ],
        [
            InlineKeyboardButton("Смесь", callback_data="coffee_blend")
        ],
        [
            InlineKeyboardButton("« Назад", callback_data="back_to_settings")
        ]
    ]
    return InlineKeyboardMarkup(keyboard) 