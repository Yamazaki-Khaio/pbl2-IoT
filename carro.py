import json
import random

def generate_car_data():
    descarga = random.choice(["rápida", "lenta"])
    dados = {
        "id": random.randint(1, 100),
        "marca": random.choice(["Tesla", "Nissan", "BMW"]),
        "modelo": random.choice(["Model S", "Leaf", "i3"]),
        "bateria": random.randint(0, 100),
        "descarga": descarga
    }

    if descarga == "rápida":
        dados["bateria"] -= random.randint(4, 6)
    else:
        dados["bateria"] -= random.randint(1, 3)

    if dados["bateria"] < 0:
        dados["bateria"] = 0

    return json.dumps(dados)
