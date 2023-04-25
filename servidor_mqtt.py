import paho.mqtt.client as mqtt
import json
import random
import time
import threading
# Configurações do MQTT broker
broker_address = "localhost"
broker_port = 1883
broker_topic = "dadoscarros"
broker_topic_posto = "dadospontos"

# Configurações do fog node
fog_ip = "localhost"
fog_port = 1883
fog_topic = "dadosfog"


# Configurações do edge node
edge_ip = "localhost"
edge_port = 1883
edge_topic = "dadosedge"

# Variáveis para controle da carga de processamento dos nós
fog_load = 0
edge_load = 0
fog_capacity = 10
edge_capacity = 5

# Função que processa os dados dos carros e publica no tópico do fog node
def process_car_data(client, userdata, message):
    try:
        payload = message.payload.decode("utf-8")
        dados = json.loads(payload)
        descarga = dados["descarga"]

        if descarga == "rápida":
            tempo = random.randint(2, 5)
        else:
            tempo = random.randint(1, 3)

        dados["tempo_carregamento"] = tempo
        print(f"Dados do carro processados: {dados}")
        client.publish(fog_topic, json.dumps(dados).encode("utf-8"), qos=1, retain=True)

        global fog_load
        fog_load += 1
    except Exception as e:
        print(f"Erro no processamento de dados do carro: {e}")





# Função que processa os dados dos postos de recarga e publica no tópico do edge node
def process_posto_data(client, userdata, message):
        try:
            payload = message.payload.decode("utf-8")
            dados = json.loads(payload)
            capacidade = dados["capacidade"]
            fila = dados["fila"]

            if fila > capacidade / 2:
                tempo = random.randint(5, 10)
            else:
                tempo = random.randint(2, 5)

            dados["tempo_espera"] = tempo
            print(f"Dados do posto de recarga processados: {dados}")
            client.publish(edge_topic, json.dumps(dados).encode("utf-8"), qos=0, retain=True)

            global edge_load
            edge_load += 1
        except Exception as e:
            print(f"Erro no processamento de dados do carro: {e}")

# Configuração do cliente MQTT e inscrição nos tópicos


client = mqtt.Client()


client.connect(broker_address, broker_port)
client.subscribe(broker_topic, qos=0)
client.subscribe(broker_topic_posto, qos=0)

# Thread para receber mensagens do broker e chamar as funções de processamento de dados
def on_message(client, userdata, message):
    if message.topic == broker_topic:
        process_car_data(client, userdata, message)
    elif message.topic == broker_topic_posto:
        process_posto_data(client, userdata, message)

client.on_message = on_message
def mqtt_loop():
    while True:
        try:
            client.loop_forever()
        except Exception as e:
            print(f"Erro ao conectar ao broker: {e}")
            time.sleep(5)

mqtt_thread = threading.Thread(target=mqtt_loop)
mqtt_thread.start()


# Loop principal para gerar e publicar dados
while True:
    time.sleep(5)