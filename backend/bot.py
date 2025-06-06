#!/usr/bin/env python3
"""
Coffee Grinder Bot - Telegram бот для рекомендации настроек кофемолок
"""

import os
import logging
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from app.bot.handlers import start, help_command, settings, recommend
from app.database import init_db

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main() -> None:
    """Запуск бота."""
    # Загрузка переменных окружения
    load_dotenv()
    
    # Инициализация базы данных
    init_db()
    
    # Создание приложения
    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("settings", settings))
    application.add_handler(CommandHandler("recommend", recommend))

    # Запуск бота
    application.run_polling(allowed_updates=Application.ALL_TYPES)

if __name__ == '__main__':
    main() 