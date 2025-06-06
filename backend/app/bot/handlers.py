"""
Обработчики команд для Telegram бота
"""

from telegram import Update
from telegram.ext import ContextTypes
from app.database.models import User, GrinderSettings
from app.bot.keyboards import get_main_keyboard, get_settings_keyboard

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start."""
    user = update.effective_user
    welcome_message = (
        f"👋 Привет, {user.first_name}!\n\n"
        "Я бот для рекомендации настроек кофемолок. "
        "Я помогу вам найти оптимальные настройки для вашей кофемолки "
        "на основе ваших предпочтений и типа кофе.\n\n"
        "Используйте /help для получения списка доступных команд."
    )
    await update.message.reply_text(welcome_message, reply_markup=get_main_keyboard())

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help."""
    help_text = (
        "📚 Доступные команды:\n\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать это сообщение\n"
        "/settings - Настройки вашей кофемолки\n"
        "/recommend - Получить рекомендации\n"
    )
    await update.message.reply_text(help_text)

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /settings."""
    settings_text = (
        "⚙️ Настройки кофемолки\n\n"
        "Выберите параметры вашей кофемолки:"
    )
    await update.message.reply_text(settings_text, reply_markup=get_settings_keyboard())

async def recommend(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /recommend."""
    # TODO: Реализовать логику рекомендаций
    recommendation = "Рекомендуемые настройки для вашей кофемолки:\n\n"
    recommendation += "• Крупность помола: средняя\n"
    recommendation += "• Время помола: 15 секунд\n"
    recommendation += "• Температура воды: 92°C"
    
    await update.message.reply_text(recommendation) 