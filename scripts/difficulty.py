from data.database import Database
from data.models import CountryInfo

db = Database()

all_europian = db.session.query(CountryInfo).filter(CountryInfo.region == 'Европа').all()
all_afrika = db.session.query(CountryInfo).filter(CountryInfo.region == 'Африка').all()
all = db.session.query(CountryInfo).all()

for country in all_afrika:
    country.difficulty = 3
    db.session.commit()