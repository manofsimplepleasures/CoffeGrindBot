"""
Инициализация базы данных
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Получение URL базы данных из переменных окружения
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/coffee_bot')

# Создание движка базы данных
engine = create_engine(DATABASE_URL)

# Создание фабрики сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание базового класса для моделей
Base = declarative_base()

def init_db():
    """Инициализация базы данных."""
    from .models import Base
    Base.metadata.create_all(bind=engine)

def get_db():
    """Получение сессии базы данных."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 