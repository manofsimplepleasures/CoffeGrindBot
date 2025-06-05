from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Text, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class BrewMethod(Base):
    __tablename__ = 'brew_methods'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(Text)
    grind_range = Column(String(50))
    
    grind_settings = relationship("GrindSetting", back_populates="brew_method")
    user_logs = relationship("UserLog", back_populates="brew_method")

class Grinder(Base):
    __tablename__ = 'grinders'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    max_clicks = Column(Integer)
    
    grind_settings = relationship("GrindSetting", back_populates="grinder")
    user_logs = relationship("UserLog", back_populates="grinder")

class GrindSetting(Base):
    __tablename__ = 'grind_settings'
    
    id = Column(Integer, primary_key=True)
    brew_method_id = Column(Integer, ForeignKey('brew_methods.id'))
    grinder_id = Column(Integer, ForeignKey('grinders.id'))
    recommended_clicks = Column(String(50))
    
    brew_method = relationship("BrewMethod", back_populates="grind_settings")
    grinder = relationship("Grinder", back_populates="grind_settings")

class UserLog(Base):
    __tablename__ = 'user_logs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    brew_method_id = Column(Integer, ForeignKey('brew_methods.id'))
    grinder_id = Column(Integer, ForeignKey('grinders.id'))
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    brew_method = relationship("BrewMethod", back_populates="user_logs")
    grinder = relationship("Grinder", back_populates="user_logs")

def init_db():
    database_url = os.getenv('DATABASE_URL', 'sqlite:///coffee_bot.db')
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()

def get_db_session():
    return init_db()

# Начальные данные
INITIAL_DATA = {
    'brew_methods': [
        {'name': 'Мока', 'description': 'Итальянский способ заваривания', 'grind_range': 'Средний-мелкий'},
        {'name': 'Фильтр', 'description': 'Капельное заваривание', 'grind_range': 'Средний'},
        {'name': 'Аэропресс', 'description': 'Заваривание под давлением', 'grind_range': 'Средний-мелкий'},
        {'name': 'Френч-пресс', 'description': 'Настаивание', 'grind_range': 'Крупный'},
        {'name': 'Эспрессо', 'description': 'Заваривание под высоким давлением', 'grind_range': 'Мелкий'}
    ],
    'grinders': [
        {'name': 'Hario Skerton', 'max_clicks': 40},
        {'name': 'Timemore C2', 'max_clicks': 30},
        {'name': 'Comandante C40', 'max_clicks': 30},
        {'name': 'Baratza Encore', 'max_clicks': 40},
        {'name': 'Fellow Ode', 'max_clicks': 31}
    ],
    'grind_settings': [
        {'brew_method': 'Мока', 'grinder': 'Hario Skerton', 'recommended_clicks': '10-15'},
        {'brew_method': 'Мока', 'grinder': 'Timemore C2', 'recommended_clicks': '8-12'},
        {'brew_method': 'Фильтр', 'grinder': 'Hario Skerton', 'recommended_clicks': '20-25'},
        {'brew_method': 'Фильтр', 'grinder': 'Timemore C2', 'recommended_clicks': '15-20'}
    ]
} 