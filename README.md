# CoffeGrindBot
Telegram-бот для кофе-энтузиастов, который помогает выбрать оптимальную степень помола для механических кофемолок. 
## Функции
- Выбор метода заваривания (мока, фильтр, аэропресс и т.д.).
- Выбор модели кофемолки (Hario, Timemore и т.д.).
- Рекомендации по количеству кликов для помола.
- Логирование запросов для аналитики.
- Веб-интерфейс на React с графиками популярности методов заваривания.
- Поддержка SQLite (локально) и PostgreSQL (продакшен).

## Структура
- `/backend` — Python (Flask, Telegram Bot, SQLAlchemy).
- `/frontend` — React (Node.js 22, Chart.js).

## Установка
### Бэкенд
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/yourusername/coffee-grind-bot.git
   cd backend
   ```
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Создайте `.env` с токеном:
   ```
   TELEGRAM_TOKEN=your_token_here
   ```
4. Запустите бэкенд:
   ```bash
   python main.py
   ```

### Фронтенд
1. Перейдите в папку фронтенда:
   ```bash
   cd frontend
   ```
2. Установите зависимости:
   ```bash
   npm install
   ```
3. Запустите локально:
   ```bash
   npm start
   ```

## Деплой на Timeweb Cloud
### Бэкенд
1. Создайте Python-приложение в Timeweb Cloud.
2. Настройте PostgreSQL и обновите `database.py` с данными подключения.
3. Загрузите файлы через Git или SFTP.
4. Установите зависимости: `pip install -r requirements.txt`.
5. Настройте вебхук:
   ```bash
   curl -F "url=https://your-backend.timeweb.cloud/webhook" https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook
   ```

### Фронтенд
1. Создайте приложение Node.js 22 (React) в Timeweb Cloud.
2. Выполните сборку: `npm run build`.
3. Загрузите файлы через Git или SFTP.
4. Настройте обслуживание `build`-папки.

## Аналитика
- Логи хранятся в таблице `user_logs`.
- Пример SQL-запроса:
  ```sql
  SELECT bm.name, COUNT(*) as count
  FROM user_logs ul
  JOIN brew_methods bm ON ul.brew_method_id = bm.id
  GROUP BY bm.name
  ORDER BY count DESC;
  ```
- Веб-интерфейс: `https://your-frontend.timeweb.cloud/analytics` показывает графики.

## Пример использования
1. Telegram-бот:
   - Запустите: `/start`.
   - Выберите метод: `/select_method`.
   - Выберите кофемолку и укажите клики.
   - Получите рекомендацию.
2. Веб-интерфейс: откройте `https://your-frontend.timeweb.cloud/analytics`.

## Технологии
- Бэкенд: Python, `python-telegram-bot`, Flask, SQLAlchemy.
- Фронтенд: React, Chart.js, Node.js 22.
- База данных: SQLite (локально), PostgreSQL (продакшен).
- Деплой: Timeweb Cloud.
- Хостинг кода: GitHub.
