from data.constants import constants
from data.database import Database
from data.models import (ContinueKeyboard, DifficultyChangingKeyboard,
                         GameKeyboard, User)
from data.utils import calculate_score
from telegram import ParseMode

from actions.stats import get_score

db = Database()
diff_description = constants['diff_description']

def game(update, context):
    user_id = update.effective_chat.id
    user = db.session.query(User).filter_by(user_id=user_id).first()
    k = GameKeyboard(user)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Как называется столица государства {k.correct_answer.name.title()}?',
        reply_markup=k.generate_keyboard_markup()
    )

def keyboard_game_handler(update, context):
    data = update.callback_query.data
    user_id = update.effective_chat.id
    user = db.session.query(User).filter_by(user_id=user_id).first()
    difficulty = user.difficulty + 1
    update.callback_query.answer()

    if data == 'start':
        update.callback_query.edit_message_text(
            text='Начинаем игру!\nИ первый вопрос:',
            )
        return game(update, context)

    if data == 'True':
        user.user_score = calculate_score(user, difficulty, True)
        db.session.commit()
        update.callback_query.edit_message_text(
            text=f'Правильно! +{difficulty} очка!\n\nТекущий счет: <b>{user.user_score}</b>',
            reply_markup=ContinueKeyboard().generate_keyboard_markup(),
            parse_mode=ParseMode.HTML)

    if data == 'False':
        user.user_score = calculate_score(user, difficulty, False)
        db.session.commit()
        update.callback_query.edit_message_text(
            text=f'К сожалению, неверно! Вы теряете {difficulty} очка!\n\nТекущий счет: <b>{user.user_score}</b>',
            reply_markup=ContinueKeyboard().generate_keyboard_markup(),
            parse_mode=ParseMode.HTML)

    if data == 'game':
        k = GameKeyboard(user)
        update.callback_query.edit_message_text(
            text=f'Как называется столица государства {k.correct_answer.name.title()}?',
            reply_markup=k.generate_keyboard_markup()
    )

    if data == 'score':
        update.callback_query.edit_message_text(
            text=get_score(user),
            reply_markup=ContinueKeyboard().generate_keyboard_markup(),
            parse_mode=ParseMode.HTML)

    if 'pass' in data:
        if user.user_score >= 1:
            user.user_score -= 1
        else:
            user.user_score = 0
        db.session.commit()
        update.callback_query.edit_message_text(
            text=f'Очень жаль😔\nПравильный ответ: <b>{data.replace("pass","")}</b>\n\nВы теряете 1 очко!\nТекущий счет: <b>{user.user_score}</b>\n',
            reply_markup=ContinueKeyboard().generate_keyboard_markup(),
            parse_mode=ParseMode.HTML)

    if data == 'change_difficulty':
        update.callback_query.edit_message_text(
            text=f'Пожалуйста, выберите уровень сложности:\n\n{diff_description}',
            reply_markup=DifficultyChangingKeyboard().generate_keyboard_markup(),
            parse_mode=ParseMode.HTML)

    if 'diff_' in data:
        if data == 'diff_1':
            user.difficulty = 1
            text = 'Простой'
        if data == 'diff_2':
            user.difficulty = 2
            text = 'Нормальный'
        if data == 'diff_3':
            user.difficulty = 3
            text = 'Сложный'

        db.session.commit()

        update.callback_query.edit_message_text(
            text=f'Выбран уровень сложности <b>{text}</b>',
            reply_markup=ContinueKeyboard().generate_keyboard_markup(),
            parse_mode=ParseMode.HTML)
