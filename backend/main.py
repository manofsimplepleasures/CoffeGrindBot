import os
import logging
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from dotenv import load_dotenv
from database import init_db, get_db_session, BrewMethod, Grinder, GrindSetting, UserLog, INITIAL_DATA

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Инициализация Flask
app = Flask(__name__)
CORS(app)

# Состояния для ConversationHandler
SELECTING_METHOD, SELECTING_GRINDER, SETTING_CLICKS = range(3)

# Инициализация базы данных
db = init_db()

# Инициализация начальных данных
def init_data():
    session = get_db_session()
    try:
        # Добавляем методы заваривания
        if not session.query(BrewMethod).first():
            for method in INITIAL_DATA['brew_methods']:
                brew_method = BrewMethod(**method)
                session.add(brew_method)
            session.commit()

        # Добавляем кофемолки
        if not session.query(Grinder).first():
            for grinder in INITIAL_DATA['grinders']:
                grinder_obj = Grinder(**grinder)
                session.add(grinder_obj)
            session.commit()

        # Добавляем настройки помола
        if not session.query(GrindSetting).first():
            for setting in INITIAL_DATA['grind_settings']:
                brew_method = session.query(BrewMethod).filter_by(name=setting['brew_method']).first()
                grinder = session.query(Grinder).filter_by(name=setting['grinder']).first()
                if brew_method and grinder:
                    grind_setting = GrindSetting(
                        brew_method_id=brew_method.id,
                        grinder_id=grinder.id,
                        recommended_clicks=setting['recommended_clicks']
                    )
                    session.add(grind_setting)
            session.commit()
    finally:
        session.close()

# Обработчики команд Telegram бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [InlineKeyboardButton("Выбрать метод заваривания", callback_data='select_method')],
        [InlineKeyboardButton("Выбрать кофемолку", callback_data='select_grinder')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет! Я помогу тебе выбрать оптимальные настройки помола для твоей кофемолки. "
        "Что ты хочешь сделать?",
        reply_markup=reply_markup
    )
    return ConversationHandler.END

async def select_method(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    session = get_db_session()
    try:
        methods = session.query(BrewMethod).all()
        keyboard = [[InlineKeyboardButton(method.name, callback_data=f'method_{method.id}')] 
                   for method in methods]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                "Выберите метод заваривания:",
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                "Выберите метод заваривания:",
                reply_markup=reply_markup
            )
        return SELECTING_METHOD
    finally:
        session.close()

async def select_grinder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    
    method_id = int(query.data.split('_')[1])
    context.user_data['brew_method_id'] = method_id
    
    session = get_db_session()
    try:
        grinders = session.query(Grinder).all()
        keyboard = [[InlineKeyboardButton(grinder.name, callback_data=f'grinder_{grinder.id}')] 
                   for grinder in grinders]
        keyboard.append([InlineKeyboardButton("Другая кофемолка", callback_data='other_grinder')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "Выберите вашу кофемолку:",
            reply_markup=reply_markup
        )
        return SELECTING_GRINDER
    finally:
        session.close()

async def set_clicks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    
    if query.data == 'other_grinder':
        await query.edit_message_text(
            "Пожалуйста, введите максимальное количество кликов вашей кофемолки:"
        )
        return SETTING_CLICKS
    
    grinder_id = int(query.data.split('_')[1])
    context.user_data['grinder_id'] = grinder_id
    
    return await get_recommendation(update, context)

async def get_recommendation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    session = get_db_session()
    try:
        if 'brew_method_id' not in context.user_data or 'grinder_id' not in context.user_data:
            await update.message.reply_text("Пожалуйста, сначала выберите метод заваривания и кофемолку.")
            return ConversationHandler.END
        
        method_id = context.user_data['brew_method_id']
        grinder_id = context.user_data['grinder_id']
        
        setting = session.query(GrindSetting).filter_by(
            brew_method_id=method_id,
            grinder_id=grinder_id
        ).first()
        
        if setting:
            # Логируем запрос
            log = UserLog(
                user_id=update.effective_user.id,
                brew_method_id=method_id,
                grinder_id=grinder_id
            )
            session.add(log)
            session.commit()
            
            await update.message.reply_text(
                f"Рекомендуемое количество кликов: {setting.recommended_clicks}"
            )
        else:
            grinder = session.query(Grinder).get(grinder_id)
            await update.message.reply_text(
                f"Для вашей кофемолки {grinder.name} максимальное количество кликов: {grinder.max_clicks}. "
                "Попробуйте настройки в диапазоне 30-70% от максимального."
            )
        
        return ConversationHandler.END
    finally:
        session.close()

# API endpoints
@app.route('/api/analytics')
def get_analytics():
    session = get_db_session()
    try:
        analytics = session.query(
            BrewMethod.name,
            func.count(UserLog.id).label('count')
        ).join(UserLog).group_by(BrewMethod.name).all()
        
        return jsonify([{
            'method': name,
            'count': count
        } for name, count in analytics])
    finally:
        session.close()

# Инициализация и запуск
def main():
    # Инициализация данных
    init_data()
    
    # Настройка Telegram бота
    application = Application.builder().token(TOKEN).build()
    
    # Добавление обработчиков
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            CommandHandler('select_method', select_method),
            CallbackQueryHandler(select_method, pattern='^select_method$')
        ],
        states={
            SELECTING_METHOD: [CallbackQueryHandler(select_grinder, pattern='^method_')],
            SELECTING_GRINDER: [CallbackQueryHandler(set_clicks, pattern='^(grinder_|other_grinder)$')],
            SETTING_CLICKS: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_clicks)]
        },
        fallbacks=[CommandHandler('start', start)]
    )
    
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('get_recommendation', get_recommendation))
    
    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main() 