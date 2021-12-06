from data.database import Database
from sqlalchemy import desc
from data.models import User

db = Database()

def get_score(player):
    users = db.session.query(User).order_by(desc(User.user_score)).limit(10).all()
    top10 = []
    for number, user in enumerate(users):
        if player.user_id == user.user_id:
            top10.append('<b>' + str(number + 1) + '. ' + user.user_name + ' - ' + str(user.user_score) + "</b>")
        else:
            top10.append(str(number + 1) + '. ' + user.user_name +' - ' + str(user.user_score))

    return '\n'.join(top10)
