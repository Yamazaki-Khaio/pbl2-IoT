import requests
import json

def localizar_posto_com_menor_fila():
    url = "http://localhost:5000/posto/fila"
    response = requests.get(url)
    postos = json.loads(response.text)

    menor_fila = None
    posto_menor_fila = None
    for posto in postos:
        if menor_fila is None or posto["num_carros"] < menor_fila:
            menor_fila = posto["num_carros"]

    return f"O posto de recarga mais próximo com a menor fila é o posto {posto_menor_fila['id']} na latitude {posto_menor_fila['latitude']} e longitude {posto_menor_fila['longitude']}."

print(localizar_posto_com_menor_fila())