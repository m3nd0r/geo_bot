from data.database import Database
from data.models import StartgameKeyboard, User
from data.utils import name_exists, user_exists
from telegram.ext import ConversationHandler

db = Database()

REG, OLD = range(2)

def start(update, context):
    user_id = update.message.chat_id
    if user_exists(user_id):
        user = db.session.query(User).filter_by(user_id=user_id).first()
        context.bot.send_message(
            chat_id=user_id,
            text=f'Привет, {user.user_name}!\n',
            reply_markup=StartgameKeyboard().generate_keyboard_markup(),
            )
    else:
        update.message.reply_text(
            'Привет, дорогой друг!👋🏻\n\nПожалуйста, введи свое игровое(или настоящее😊) имя\nПод этим именем твои результаты будут отображаться в Таблице Лучших!')
        return REG


def registration(update, context):
    name = update.message.text
    user_id = update.message.chat_id

    if not name_exists(name):
        db.session.add(User(
            user_id=user_id,
            user_name=name,
            user_score=0)
        )
        db.session.commit()
        update.message.reply_text(
            f'Спасибо! Теперь Вы известны как {name}!\nМожно начинать игру.',
            reply_markup=StartgameKeyboard().generate_keyboard_markup()
        )
        return ConversationHandler.END
    else:
        update.message.reply_text(
            'Прошу прощения, но имя уже занято. Попробуйте другое.')
        return REG

def unknown(update, context):
    update.message.reply_text(
        "Извините, не знаю такой команды😔\n"
        )

def done(update, context):
    update.message.reply_text('Завершение процесса...')
    return ConversationHandler.END
