import threading
import uuid
import paho.mqtt.client as mqtt
import json
import random
import time

# Configurações do MQTT broker
broker_address = "172.16.103.13"
broker_port = 1883
broker_topic = "dadoscarros"
broker_topic_posto = "dadospontos"

# Bairros onde os carros podem se deslocar
bairros = ["Brasília", "Caseb", "Centro", "Feira IV", "George Américo", "Jardim Acácia", "Jardim Cruzeiro", "Kalilândia", "Mangabeira", "Muchila", "Papagaio", "Parque Getúlio Vargas", "Queimadinha", "Santa Mônica", "UEFS", "Santo Antônio dos Prazeres", "Serraria Brasil", "SIM", "Tomba"]

# Locais onde os postos podem ser instalados
locais = ["Brasília", "Caseb", "Centro", "Feira IV", "George Américo", "Jardim Acácia", "Jardim Cruzeiro", "Kalilândia", "Mangabeira", "Muchila", "Papagaio", "Parque Getúlio Vargas", "Queimadinha", "Santa Mônica", "Santo Antônio dos Prazeres", "Serraria Brasil", "SIM", "Tomba"]



def get_localizacao(bairro):
    if bairro in ["Centro", "UEFS", "Brasília"]:
        return "fog"
    else:
        return "edge"



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

    return dados

def generate_posto_data(localizacao):
    dados = {
        "id":str(uuid.uuid1()),
        "capacidade": random.randint(50, 100),
        "fila": random.randint(0, 50),
        "localizacao": localizacao,
        "tipo": ""
    }
    if localizacao in ["Centro", "UEFS", "Brasília"]:
        dados["tipo"] = "fog"
    else:
        dados["tipo"] = "edge"

    return dados


def simular_carro(bairro, broker_topic):
    dados = generate_car_data()
    dados["bairro"] = bairro
    dados["localizacao"] = get_localizacao(bairro)
    print(f"Carro {dados['id']} está no bairro {bairro} com {dados['bateria']}% de bateria.")
    while dados["bateria"] > 0:
        dados["bateria"] -= random.randint(1, 3)
        if dados["bateria"] < 0:
            dados["bateria"] = 0
        print(f"Carro {dados['id']} está no bairro {dados['bairro']} com {dados['bateria']}% de bateria.")
        if random.randint(0, 10) == 0:
            novo_bairro = random.choice(bairros)
            dados["bairro"] = novo_bairro
            dados["localizacao"] = get_localizacao(novo_bairro)
            print(f"Carro {dados['id']} mudou para o bairro {novo_bairro}.")
        
        # Verifica se o carro está em uma localização de fog ou edge computing
        if dados["localizacao"] in ["Centro", "UEFS", "Brasília"]:
            dados["tipo"] = "carro"
            current_topic = "fog"
        else:
            dados["tipo"] = "carro"
            current_topic = "edge"
        
        # Publique os dados do carro no tópico MQTT correspondente
        payload = json.dumps(dados)
        client.publish(current_topic, payload.encode("utf-8"), qos=0)
        print(f"Enviando o seguinte payload para o tópico {current_topic}:")
        print(payload)

        # Aguarde um tempo antes de continuar a simulação
        time.sleep(5)


def simular_posto(localizacao, broker_topic):
    posto_data = generate_posto_data(localizacao)
    print(f"Posto {posto_data['id']} está na localização {localizacao} com {posto_data['capacidade']} de capacidade e fila inicial de {posto_data['fila']}.")
    while True:
        # Atualiza a fila do posto
        posto_data["fila"] += random.randint(-5, 5)
        if posto_data["fila"] < 0:
            posto_data["fila"] = 0
        if posto_data["fila"] > posto_data["capacidade"]:
            posto_data["fila"] = posto_data["capacidade"]

        # Verifica se o posto está em uma localização de fog ou edge computing
        if posto_data["localizacao"] in ["Centro", "UEFS", "Brasília"]:
            posto_data["tipo"] = "posto"
            current_topic = "fog"
        else:
            posto_data["tipo"] = "posto"
            current_topic = "edge"

        # Publica os dados atualizados do posto no tópico MQTT correspondente
        payload = json.dumps(posto_data)
        client.publish(current_topic, payload.encode("utf-8"), qos=0)
        print(f"Enviando o seguinte payload atualizado do posto para o tópico {current_topic}:")
        print(payload)

        # Aguarda um tempo antes de continuar a simulação
        time.sleep(5)


# Configuração do cliente MQTT e inscrição nos tópicos
client = mqtt.Client()
client.connect(broker_address, broker_port, 60)
client.subscribe(broker_topic, qos=1)
client.subscribe(broker_topic_posto, qos=1)
# Função que lida com os dados dos carros recebidos do broker
def handle_car_data(client, userdata, message):
    payload = message.payload.decode("utf-8")
    print(f"Dados do carro recebidos: {payload}")

# Função que lida com os dados dos postos de combustível recebidos do broker
def handle_posto_data(client, userdata, message):
    payload = message.payload.decode("utf-8")
    print(f"Dados do posto de combustível recebidos: {payloada}")


# Callback para receber mensagens do broker e chamar as funções de tratamento de dados
def on_message(client, userdata, message):
    if message.topic == broker_topic:
        handle_car_data(client, userdata, message)
    elif message.topic == broker_topic_posto:
        handle_posto_data(client, userdata, message)

client.on_message = on_message
client.loop_start()

# Loop principal para gerar e publicar dados do posto
# Função principal da thread de simulação do posto
def simular_posto_thread(bairro, broker_topic_posto):
    while True:
        simular_posto(bairro, broker_topic_posto)
        time.sleep(5)

# Função principal da thread de simulação do carro
def simular_carro_thread(bairro, broker_topic):
    while True:
        simular_carro(bairro, broker_topic)
        time.sleep(5)

# Criação e inicialização das threads
posto_thread = threading.Thread(target=simular_posto_thread, args=("UEFS", "dadospostos"))
carro_thread = threading.Thread(target=simular_carro_thread, args=("UEFS", "dadoscarros"))
posto_thread.start()
carro_thread.start()