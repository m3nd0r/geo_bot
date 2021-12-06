import random

import environs
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from data.database import Database
from data.modelMixins import KeyboardMixin

env = environs.Env()
Base = declarative_base()
db = Database()


class User(Base):
    """
    Базовая модель Пользователя
    """
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    user_name = Column(String)
    user_score = Column(Integer)
    difficulty = Column(Integer, default=1)

    def __repr__(self):
        return f"<User {self.id}, {self.user_name}, {self.user_score}>"


class CountryInfo(Base):
    """
    Базовая модель стран
    """
    __tablename__ = 'country_info'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    capital = Column(String)
    region = Column(String)
    difficulty = Column(Integer)

    def __repr__(self):
        return f"<CountryInfo {self.name}, {self.id}>"

# Base.metadata.create_all(db.engine)


class GameKeyboard(KeyboardMixin):
    def __init__(self, user):
        self.user = user
        self.keyboard_dict = self.generating_keyboard()
        self.buttons_in_row = 2
        self.correct_answer = [k for k, v in self.keyboard_dict.items() if v == 'True'][0]

    def generating_keyboard(self):
        country_list = random.sample(db.session.query(CountryInfo).filter_by(difficulty=self.user.difficulty).all(), 4)
        # country_list = [db.session.query(CountryInfo).filter_by(id=id).first() for id in id_list]
        correct_answer = random.choice(country_list)
        keyboard = {}

        for country in country_list:
            keyboard.update({
                country : str(bool(country == correct_answer)),
            })
        return keyboard

    def generate_keyboard_markup(self):
        """
        Собираем разметку и запоминаем нажатые кнопки
        """
        keyboard = list()
        rows = list()
        buttons_list = list()
        for button, data in self.keyboard_dict.items():
            buttons_list.append(InlineKeyboardButton(button.capital, callback_data=data))

        i = 0
        for i in range(len(buttons_list)):
            rows.append(buttons_list[i])
            i += 1
            if i % self.buttons_in_row == 0:
                keyboard.append(rows[:i])
                rows = []

        last_row_button_num = len(self.keyboard_dict.keys()) % self.buttons_in_row
        if last_row_button_num != 0:
            keyboard.append(buttons_list[-last_row_button_num:])
        keyboard.append([InlineKeyboardButton('Сдаюсь', callback_data='pass' + str(self.correct_answer.capital.title()))])
        markup = InlineKeyboardMarkup(keyboard)

        return markup


class StartgameKeyboard(KeyboardMixin):
    def __init__(self):
        self.keyboard_dict = {
            'Начать игру!': 'start',
        }
        self.buttons_in_row = 1


class ContinueKeyboard(KeyboardMixin):
    def __init__(self):
        self.keyboard_dict = {
            'Следующий вопрос:': 'game',
            'Таблица Лучших': 'score',
            'Сменить сложность': 'change_difficulty',
        }
        self.buttons_in_row = 2


class DifficultyChangingKeyboard(KeyboardMixin):
    def __init__(self):
        self.keyboard_dict = {
            'Простая': 'diff_1',
            'Нормальная': 'diff_2',
            'Сложная': 'diff_3',
        }
        self.buttons_in_row = 3