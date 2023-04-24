import paho.mqtt.client as mqtt
import json
import random
import time

car_id = "car1"  # identificador do carro
topic = "dadoscarros"
latitude = -23.5489  # latitude do carro
longitude = -46.6388  # longitude do carro
battery_level = 100  # nível de bateria inicial

# cria um cliente MQTT
client = mqtt.Client()

# conecta ao broker MQTT
client.connect("localhost", 1883, 60)

# loop para enviar as mensagens periodicamente
while True:
    # simula a movimentação do carro
    latitude += random.uniform(-0.001, 0.001)
    longitude += random.uniform(-0.001, 0.001)

    # simula o consumo de bateria
    battery_level -= random.randint(1, 5)

    # cria um dicionário com as informações do carro
    car_data = {"id": car_id, "latitude": latitude, "longitude": longitude, "battery_level": battery_level}

    # converte o dicionário para um objeto JSON
    message = json.dumps(car_data)

    # publica a mensagem no tópico 'carros'
    client.publish(topic, message.encode("utf-8"))

    # espera um intervalo de 5 segundos
    time.sleep(5)
