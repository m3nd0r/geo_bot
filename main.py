import environs
from telegram import Bot
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater, CallbackQueryHandler,
                          ConversationHandler)
from actions.start import start, unknown, registration, done
from actions.game import game, keyboard_game_handler
from actions.admin import admin_check_score

env = environs.Env()

REG, OLD = range(2)

def main():
    # 1 -- Подключаемся
    bot = Bot(token=env('TOKEN'),)

    # 2 -- Обработчики
    updater = Updater(bot=bot, use_context=True,)
    dispatcher = updater.dispatcher

    start_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            REG: [MessageHandler(Filters.text, registration)],
            OLD: [],
        },
        fallbacks=[CommandHandler('done', done)],
    )
    dispatcher.add_handler(start_handler)

    game_handler = CommandHandler('game', game)
    dispatcher.add_handler(game_handler)

    keyboard_handler = CallbackQueryHandler(callback=keyboard_game_handler, pass_chat_data=True)
    dispatcher.add_handler(keyboard_handler)

    admin_check_score_handler = CommandHandler('check_score', admin_check_score)
    dispatcher.add_handler(admin_check_score_handler)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    # 3 -- Запускаем лонгпулл
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
