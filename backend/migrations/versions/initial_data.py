"""initial data

Revision ID: 002
Revises: 001
Create Date: 2024-03-20 12:01:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    # Добавление методов заваривания
    brew_methods = [
        {'name': 'V60', 'description': 'Японский метод заваривания с использованием бумажного фильтра'},
        {'name': 'Chemex', 'description': 'Метод заваривания с использованием специального стеклянного сосуда'},
        {'name': 'AeroPress', 'description': 'Метод заваривания с использованием давления'},
        {'name': 'Френч-пресс', 'description': 'Метод заваривания с использованием металлического фильтра'},
        {'name': 'Мока-пот', 'description': 'Итальянский метод заваривания с использованием давления пара'}
    ]
    
    for method in brew_methods:
        op.execute(
            "INSERT INTO brew_methods (name, description) VALUES (%s, %s)",
            (method['name'], method['description'])
        )

    # Добавление кофемолок
    grinders = [
        {'name': 'Comandante', 'model': 'C40', 'description': 'Ручная кофемолка премиум-класса'},
        {'name': 'Timemore', 'model': 'C2', 'description': 'Бюджетная ручная кофемолка'},
        {'name': 'Baratza', 'model': 'Encore', 'description': 'Электрическая кофемолка для дома'},
        {'name': 'Wilfa', 'model': 'Uniform', 'description': 'Электрическая кофемолка премиум-класса'}
    ]
    
    for grinder in grinders:
        op.execute(
            "INSERT INTO grinders (name, model, description) VALUES (%s, %s, %s)",
            (grinder['name'], grinder['model'], grinder['description'])
        )

    # Добавление настроек помола
    grind_settings = [
        # Comandante C40
        {'brew_method': 'V60', 'grinder': 'Comandante', 'model': 'C40', 'clicks': 24, 'description': 'Средний помол'},
        {'brew_method': 'Chemex', 'grinder': 'Comandante', 'model': 'C40', 'clicks': 28, 'description': 'Средне-крупный помол'},
        {'brew_method': 'AeroPress', 'grinder': 'Comandante', 'model': 'C40', 'clicks': 18, 'description': 'Средне-мелкий помол'},
        {'brew_method': 'Френч-пресс', 'grinder': 'Comandante', 'model': 'C40', 'clicks': 32, 'description': 'Крупный помол'},
        {'brew_method': 'Мока-пот', 'grinder': 'Comandante', 'model': 'C40', 'clicks': 12, 'description': 'Мелкий помол'},
        
        # Timemore C2
        {'brew_method': 'V60', 'grinder': 'Timemore', 'model': 'C2', 'clicks': 18, 'description': 'Средний помол'},
        {'brew_method': 'Chemex', 'grinder': 'Timemore', 'model': 'C2', 'clicks': 22, 'description': 'Средне-крупный помол'},
        {'brew_method': 'AeroPress', 'grinder': 'Timemore', 'model': 'C2', 'clicks': 14, 'description': 'Средне-мелкий помол'},
        {'brew_method': 'Френч-пресс', 'grinder': 'Timemore', 'model': 'C2', 'clicks': 26, 'description': 'Крупный помол'},
        {'brew_method': 'Мока-пот', 'grinder': 'Timemore', 'model': 'C2', 'clicks': 10, 'description': 'Мелкий помол'},
        
        # Baratza Encore
        {'brew_method': 'V60', 'grinder': 'Baratza', 'model': 'Encore', 'clicks': 20, 'description': 'Средний помол'},
        {'brew_method': 'Chemex', 'grinder': 'Baratza', 'model': 'Encore', 'clicks': 24, 'description': 'Средне-крупный помол'},
        {'brew_method': 'AeroPress', 'grinder': 'Baratza', 'model': 'Encore', 'clicks': 16, 'description': 'Средне-мелкий помол'},
        {'brew_method': 'Френч-пресс', 'grinder': 'Baratza', 'model': 'Encore', 'clicks': 28, 'description': 'Крупный помол'},
        {'brew_method': 'Мока-пот', 'grinder': 'Baratza', 'model': 'Encore', 'clicks': 12, 'description': 'Мелкий помол'},
        
        # Wilfa Uniform
        {'brew_method': 'V60', 'grinder': 'Wilfa', 'model': 'Uniform', 'clicks': 22, 'description': 'Средний помол'},
        {'brew_method': 'Chemex', 'grinder': 'Wilfa', 'model': 'Uniform', 'clicks': 26, 'description': 'Средне-крупный помол'},
        {'brew_method': 'AeroPress', 'grinder': 'Wilfa', 'model': 'Uniform', 'clicks': 18, 'description': 'Средне-мелкий помол'},
        {'brew_method': 'Френч-пресс', 'grinder': 'Wilfa', 'model': 'Uniform', 'clicks': 30, 'description': 'Крупный помол'},
        {'brew_method': 'Мока-пот', 'grinder': 'Wilfa', 'model': 'Uniform', 'clicks': 14, 'description': 'Мелкий помол'}
    ]
    
    for setting in grind_settings:
        op.execute("""
            INSERT INTO grind_settings (brew_method_id, grinder_id, clicks, description)
            SELECT 
                (SELECT id FROM brew_methods WHERE name = %s),
                (SELECT id FROM grinders WHERE name = %s AND model = %s),
                %s,
                %s
        """, (
            setting['brew_method'],
            setting['grinder'],
            setting['model'],
            setting['clicks'],
            setting['description']
        ))


def downgrade():
    # Удаление настроек помола
    op.execute("DELETE FROM grind_settings")
    
    # Удаление кофемолок
    op.execute("DELETE FROM grinders")
    
    # Удаление методов заваривания
    op.execute("DELETE FROM brew_methods") 