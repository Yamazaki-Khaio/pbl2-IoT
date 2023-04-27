import paho.mqtt.client as mqtt
import json
import random
import time
import threading

# Configurações do MQTT broker
broker_address = "172.16.103.13"
broker_port = 1883
broker_topic = "dadoscarros"
broker_topic_posto = "dadospontos"


# Variáveis para controle da carga de processamento dos nós
fog_load = 0
edge_load = 0
fog_capacity = 10
edge_capacity = 5


# Lock para proteger as variáveis de carga
lock = threading.Lock()


# Função que processa os dados dos carros e publica no tópico do fog node
def process_car_data(client, userdata, message):
    try:
        payload = message.payload.decode("utf-8")
        dados = json.loads(payload)
        descarga = dados.get("descarga")

        if descarga == "rápida":
            tempo = random.randint(2, 5)
        else:
            tempo = random.randint(1, 3)

        dados["tempo_carregamento"] = tempo
        print(f"Dados do carro processados: {dados}")
        global fog_load, edge_load
        with lock:
            if dados["localizacao"] == "fog" and fog_load < fog_capacity:
                client.publish("fog", json.dumps(dados).encode("utf-8"), qos=1, retain=True)
                fog_load += 1
            else:
                client.publish("edge", json.dumps(dados).encode("utf-8"), qos=0, retain=True)
                edge_load += 1

        time.sleep(3)
    except Exception as e:
        print(f"Erro no processamento de dados do carro: {e}")

# Função que processa os dados dos postos de recarga e publica no tópico do edge node
def process_posto_data(client, userdata, message):
        try:
            payload = message.payload.decode("utf-8")
            dados = json.loads(payload)
            capacidade = dados.get("capacidade")
            fila = dados.get("fila")

            if fila > capacidade / 2:
                tempo = random.randint(5, 10)
            else:
                tempo = random.randint(2, 5)

            dados["tempo_espera"] = tempo
            print(f"Dados do posto de recarga processados: {dados}")
            global edge_load, fog_load
            with lock:
                if edge_load < edge_capacity:
                    client.publish("edge", json.dumps(dados).encode("utf-8"), qos=0, retain=True)
                    edge_load += 1
                else:
                    client.publish("fog", json.dumps(dados).encode("utf-8"), qos=1, retain=True)
                    fog_load += 1

            time.sleep(3)
        except Exception as e:
            print(f"Erro no processamento de dados do posto de recarga: {e}")

# Callback que é chamado quando um novo payload é recebido no tópico MQTT correspondente

def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode("utf-8")
    dados = json.loads(payload)
    tipo = dados.get("tipo")

    if topic == "fog" or topic == "edge" and tipo == "carro":
        process_car_data(client, userdata, message)
    elif topic == "fog" or topic == "edge" and tipo == "posto":
        process_posto_data(client, userdata, message)
    elif topic == broker_topic_posto:
        process_posto_data(client, userdata, message)
    elif topic == broker_topic:
        process_car_data(client, userdata, message)

def adjust_capacity(load_percent, capacity, min_load, max_load, increment, decrement):
    if load_percent > max_load and capacity < min_load:
        capacity += increment
        print("Capacidade aumentada")
    elif load_percent < min_load and capacity > max_load:
        capacity -= decrement
        print("Capacidade diminuída")
    return capacity


def monitor_load():
    global fog_load, edge_load, fog_capacity, edge_capacity
    while True:
        # Monitorar a carga dos nós
        fog_load_percent = fog_load / fog_capacity * 100 if fog_capacity != 0 else 0
        edge_load_percent = edge_load / edge_capacity * 100 if edge_capacity != 0 else 0
        print(f"Carga na névoa: {fog_load}, carga na borda: {edge_load}")
        print(f"Capacidade na névoa: {fog_capacity}, capacidade na borda: {edge_capacity}")
        print(f"Porcentagem de carga na névoa: {fog_load_percent}%, porcentagem de carga na borda: {edge_load_percent}%")

        # Ajustar a capacidade de acordo com a carga
        fog_capacity = adjust_capacity(fog_load_percent, fog_capacity, 30, 70, 5, 5)
        edge_capacity = adjust_capacity(edge_load_percent, edge_capacity, 30, 70, 3, 3)

        time.sleep(5)

def main():
    # Configuração do cliente MQTT e inscrição nos tópicos
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(broker_address, broker_port, 60)
    client.subscribe("fog", qos=1)
    client.subscribe("edge", qos=1)
    client.subscribe(broker_topic, qos=0)
    client.subscribe(broker_topic_posto, qos=0)
    # Inicia a thread do monitor de carga
    monitor_thread = threading.Thread(target=monitor_load)
    monitor_thread.start()
    # Inicia a thread do cliente MQTT
    mqtt_thread = threading.Thread(target=client.loop_forever)
    mqtt_thread.start()



if __name__ == "__main__":
    main()