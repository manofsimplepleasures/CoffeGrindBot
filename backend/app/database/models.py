"""
Модели базы данных
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class GrindSize(enum.Enum):
    VERY_FINE = "very_fine"
    FINE = "fine"
    MEDIUM = "medium"
    COARSE = "coarse"
    VERY_COARSE = "very_coarse"

class CoffeeType(enum.Enum):
    ARABICA = "arabica"
    ROBUSTA = "robusta"
    BLEND = "blend"

class BrewMethod(enum.Enum):
    ESPRESSO = "espresso"
    POUR_OVER = "pour_over"
    FRENCH_PRESS = "french_press"
    AERO_PRESS = "aero_press"
    COLD_BREW = "cold_brew"

class User(Base):
    """Модель пользователя."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    settings = relationship("GrinderSettings", back_populates="user")

class GrinderSettings(Base):
    """Модель настроек кофемолки."""
    __tablename__ = 'grinder_settings'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    grind_size = Column(Enum(GrindSize))
    grind_time = Column(Float)  # в секундах
    coffee_type = Column(Enum(CoffeeType))
    brew_method = Column(Enum(BrewMethod))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="settings")

class Recommendation(Base):
    """Модель рекомендаций."""
    __tablename__ = 'recommendations'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    grind_size = Column(Enum(GrindSize))
    grind_time = Column(Float)
    coffee_type = Column(Enum(CoffeeType))
    brew_method = Column(Enum(BrewMethod))
    rating = Column(Integer)  # оценка пользователя (1-5)
    created_at = Column(DateTime, default=datetime.utcnow) 