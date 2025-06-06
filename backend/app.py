"""
Flask API для аналитики кофемолок
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from app.database import get_db
from app.database.models import User, GrinderSettings, Recommendation
from sqlalchemy import func
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

@app.route('/api/stats/users', methods=['GET'])
def get_user_stats():
    """Получение статистики пользователей."""
    db = next(get_db())
    
    total_users = db.query(User).count()
    new_users_today = db.query(User).filter(
        User.created_at >= datetime.utcnow() - timedelta(days=1)
    ).count()
    
    return jsonify({
        'total_users': total_users,
        'new_users_today': new_users_today
    })

@app.route('/api/stats/recommendations', methods=['GET'])
def get_recommendation_stats():
    """Получение статистики рекомендаций."""
    db = next(get_db())
    
    # Получение популярных настроек
    popular_settings = db.query(
        GrinderSettings.grind_size,
        GrinderSettings.coffee_type,
        GrinderSettings.brew_method,
        func.count(GrinderSettings.id).label('count')
    ).group_by(
        GrinderSettings.grind_size,
        GrinderSettings.coffee_type,
        GrinderSettings.brew_method
    ).order_by(func.count(GrinderSettings.id).desc()).limit(5).all()
    
    return jsonify({
        'popular_settings': [
            {
                'grind_size': setting.grind_size.value,
                'coffee_type': setting.coffee_type.value,
                'brew_method': setting.brew_method.value,
                'count': setting.count
            }
            for setting in popular_settings
        ]
    })

@app.route('/api/analytics/ratings', methods=['GET'])
def get_rating_analytics():
    """Получение аналитики по оценкам рекомендаций."""
    db = next(get_db())
    
    # Получение средних оценок по типам кофе
    ratings_by_coffee = db.query(
        Recommendation.coffee_type,
        func.avg(Recommendation.rating).label('avg_rating')
    ).group_by(Recommendation.coffee_type).all()
    
    return jsonify({
        'ratings_by_coffee': [
            {
                'coffee_type': rating.coffee_type.value,
                'average_rating': float(rating.avg_rating)
            }
            for rating in ratings_by_coffee
        ]
    })

@app.route('/api/analytics/trends', methods=['GET'])
def get_trends():
    """Получение трендов использования."""
    db = next(get_db())
    
    # Получение тренда использования по дням
    daily_usage = db.query(
        func.date(Recommendation.created_at).label('date'),
        func.count(Recommendation.id).label('count')
    ).group_by(
        func.date(Recommendation.created_at)
    ).order_by(
        func.date(Recommendation.created_at)
    ).all()
    
    return jsonify({
        'daily_usage': [
            {
                'date': usage.date.isoformat(),
                'count': usage.count
            }
            for usage in daily_usage
        ]
    })

if __name__ == '__main__':
    app.run(debug=True) 