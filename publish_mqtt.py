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
def gerar_dados_carro():
    # Simulação da descarga da bateria (rápida, lenta, etc.)
    descarga = random.choice(["rápida", "lenta"])
    # Geração de dados aleatórios do carro
    dados = {
        "id": random.randint(1, 100),
        "marca": random.choice(["Tesla", "Nissan", "BMW"]),
        "modelo": random.choice(["Model S", "Leaf", "i3"]),
        "bateria": random.randint(0, 100),
        "descarga": descarga
    }

    # Decrementa a bateria de acordo com a descarga
    if descarga == "rápida":
        dados["bateria"] -= random.randint(4, 6)
    else:
        dados["bateria"] -= random.randint(1, 3)

    # Garante que a bateria não seja menor que zero
    if dados["bateria"] < 0:
        dados["bateria"] = 0

    return json.dumps(dados)

def gerar_dados_posto():
    dados = {
        "id": random.randint(1, 100),
        "capacidade": random.randint(50, 100),
        "fila": random.randint(0, 50),
        "localizacao": ""
    }
    while dados["localizacao"] not in bairros:
        dados["localizacao"] = random.choice(bairros)
    return json.dumps(dados)



# Configuração do cliente MQTT e publicação de mensagens
client = mqtt.Client()
client.connect(broker_address, broker_port)

while True:
    payload = gerar_dados_carro()
    payload_pontos = gerar_dados_posto()
    client.publish(broker_topic, payload.encode("utf-8"))
    client.publish(broker_topic_posto, payload_pontos.encode("utf-8"))
    print(f"Enviando o seguinte payload para o tópico {broker_topic}:")
    print(f"Enviando o seguinte payload para o tópico {broker_topic_posto}:")
    print(payload)
    print(payload_pontos)
    time.sleep(5)
