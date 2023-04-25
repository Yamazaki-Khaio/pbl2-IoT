import paho.mqtt.client as mqtt
import json
import random
import time

ponto_recarga_id = "ponto1"  # identificador do ponto de recarga
topic = "dadospontos"
latitude = -23.5489  # latitude do ponto de recarga
longitude = -46.6388  # longitude do ponto de recarga
availability = True  # disponibilidade inicial

# cria um cliente MQTT
client = mqtt.Client()

# conecta ao broker MQTT
client.connect("localhost", 1883, 60)

# loop para enviar as mensagens periodicamente
while True:
    # simula a movimentação do ponto de recarga
    latitude += random.uniform(-0.001, 0.001)
    longitude += random.uniform(-0.001, 0.001)

    # simula a disponibilidade do ponto de recarga
    availability = bool(random.getrandbits(1))

    # cria um dicionário com as informações do ponto de recarga
    ponto_recarga_data = {"id": ponto_recarga_id, "latitude": latitude, "longitude": longitude, "availability": availability}

    # converte o dicionário para um objeto JSON
    message = json.dumps(ponto_recarga_data)

    # publica a mensagem no tópico 'pontos_recarga'
    client.publish(topic, message)

    # espera um intervalo de 10 segundos
    time.sleep(10)
