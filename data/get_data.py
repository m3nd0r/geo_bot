import requests
from database import Database
from bs4 import BeautifulSoup

from models import CountryInfo

db = Database()

def parse_data():
    response = requests.get('https://geo.koltyrin.ru/strany_mira.php')
    soup = BeautifulSoup(response.content, 'lxml')

    table = soup.find('table', class_='list')
    rows = table.find_all('tr')[1:]

    countries = []

    for row in rows:
        cols = row.find_all('td')

        countries.append({
            'name': cols[0].a.text,
            'capital': cols[1].text,
            'region': cols[4].text,
        })

    for country in countries:
        db.session.add(CountryInfo(
            name=country['name'],
            capital=country['capital'],
            region=country['region'],
        ))

    # db.session.commit()

# parse_data()