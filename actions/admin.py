import environs
from data.utils import restricted

from actions.stats import get_score

env = environs.Env()

@restricted
def admin_get_user(update, context):
    """
    Выбрать пользователя для дальнейших действий
    """
    pass


@restricted
def admin_check_score(update, context):
    """
    Посмотреть таблицу лучших
    """
    context.bot.send_message(
        chat_id=env("ADMIN_ID"),
        text=f'{get_score(player=env("ADMIN_ID"))}'
        )
