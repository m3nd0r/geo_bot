from functools import wraps

import environs

from data.database import Database
from data.models import User

env = environs.Env()
db = Database()

def restricted(func):
    """
    Дает указанном в .env ID доступ к функционалу бота. Использование:
    @restricted
    def handler(update, context):
        ...
    """
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id != env('ADMIN_ID'):
            update.message.reply_text('Доступ запрещён.\n'\
                'Автор бота @m3nd0r')
            print(user_id)
            return
        return func(update, context, *args, **kwargs)
    return wrapped

def user_exists(user_id):
    return bool(db.session.query(User).filter_by(user_id=user_id).first())

def name_exists(name):
    return bool(db.session.query(User).filter_by(user_name=name).first())

def calculate_score(user_object, difficulty, correct):
    score = user_object.user_score
    if correct:
        score += difficulty
    else:
        score -= difficulty
        if score <= 0:
            score = 0
    return score