import random

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['db-progetto']
collezione = db.sensori
list = ["True","False"]

for x in range(1,30):

    actual_date= f"2019-06-{x}"
    temperatura = random.randint(20,35)
    umidita = random.randint(20, 35)
    actual_time = "12:00"
    water = random.choice(list)
    light = random.choice(list)
    dato= {
        'water': water,
        'light': light,
        'external temperature': temperatura,
        'external humidity': umidita,
        'data': actual_date,
        'time': actual_time,
        'code': '#123abc'
    }

    collezione.insert_one(dato)

for x in range(10,24):

    actual_time= f"{x}:00"
    temperatura = random.randint(20,35)
    umidita = random.randint(20, 35)
    actual_date = "2019-06-30"
    water = random.choice(list)
    light = random.choice(list)
    dato= {
        'water': "True",
        'light': "True",
        'external temperature': temperatura,
        'external humidity': umidita,
        'data': actual_date,
        'time': actual_time,
        'code': '#123abc'
    }

    collezione.insert_one(dato)
