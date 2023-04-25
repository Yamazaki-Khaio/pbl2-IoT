import uuid
import paho.mqtt.client as mqtt
import json
import random
import time

# Configurações do MQTT broker
broker_address = "localhost"
broker_port = 1883
broker_topic = "dadoscarros"
broker_topic_posto = "dadospontos"

bairros = ["Brasília", "Caseb", "Centro", "Feira IV", "George Américo", "Jardim Acácia", "Jardim Cruzeiro", "Kalilândia", "Mangabeira", "Muchila", "Papagaio", "Parque Getúlio Vargas", "Queimadinha", "Santa Mônica", "Santo Antônio dos Prazeres", "Serraria Brasil", "SIM", "Tomba"]

# Função que gera dados aleatórios dos carros elétricos
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

def generate_posto_data():
    fila = random.randint(0, 100)
    dados = {
        "id":str(uuid.uuid1()),
        "capacidade": random.randint(50, 100),
        "fila": random.randint(0, 50),
        "localizacao": ""
    }
    while dados["localizacao"] not in bairros:
        dados["localizacao"] = random.choice(bairros)
    return json.dumps(dados)

# Função que lida com os dados dos carros recebidos do broker
def handle_car_data(client, userdata, message):
    payload = message.payload.decode("utf-8")
    print(f"Dados do carro recebidos: {payload}")

# Função que lida com os dados dos postos de combustível recebidos do broker
def handle_posto_data(client, userdata, message):
    payload = message.payload.decode("utf-8")
    print(f"Dados do posto de combustível recebidos: {payload}")

# Configuração do cliente MQTT e inscrição nos tópicos
client = mqtt.Client()
client.connect(broker_address, broker_port)
client.subscribe(broker_topic)
client.subscribe(broker_topic_posto)

# Thread para receber mensagens do broker e chamar as funções de tratamento de dados
def on_message(client, userdata, message):
    if message.topic == broker_topic:
        handle_car_data(client, userdata, message)
    elif message.topic == broker_topic_posto:
        handle_posto_data(client, userdata, message)

client.on_message = on_message
client.loop_start()

# Loop principal para gerar e publicar dados
while True:
    car_data = generate_car_data()
    posto_data = generate_posto_data()
    client.publish(broker_topic, car_data.encode("utf-8"))
    client.publish(broker_topic_posto, posto_data.encode("utf-8"))
    print(f"Enviando o seguinte payload para o tópico {broker_topic}:")
    print(car_data)
    print(f"Enviando o seguinte payload para o tópico {broker_topic_posto}:")
    print(posto_data)
    time.sleep(5)