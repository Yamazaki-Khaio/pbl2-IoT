import random
import time
import json
import paho.mqtt.client as mqtt

# Define as configurações do MQTT
broker_address = "localhost"
client_id = "carro01"
topic = "carro/01"
qos = 1
retain = False

# Função de callback para o evento de conexão ao broker MQTT
def on_connect(client, userdata, flags, rc):
    print("Conectado ao broker MQTT com sucesso. Código de retorno: " + str(rc))

# Função de callback para o evento de envio de mensagem
def on_publish(client, userdata, mid):
    print("Mensagem enviada com sucesso. ID: " + str(mid))

# Configura o cliente MQTT
client = mqtt.Client(client_id)

# Configura as funções de callback
client.on_connect = on_connect
client.on_publish = on_publish

# Conecta ao broker MQTT
client.connect(broker_address)

# Loop principal do programa
while True:
    # Gera um valor aleatório de descarga de bateria
    descarga = random.uniform(0, 1)

    # Define a tendência da descarga da bateria
    if descarga < 0.3:
        tendencia = "rápida"
    elif descarga < 0.6:
        tendencia = "média"
    else:
        tendencia = "lenta"

    # Cria um dicionário com os dados da bateria
    dados = {
        "descarga": descarga,
        "tendencia": tendencia
    }

    # Converte o dicionário para JSON
    payload = json.dumps(dados, ensure_ascii=False).encode('utf-8')

    # Envia os dados para o broker MQTT
    result, mid = client.publish(topic, payload, qos=qos, retain=retain)

    # Verifica se o envio foi bem-sucedido
    if result == mqtt.MQTT_ERR_SUCCESS:
        print("Dados enviados com sucesso. Tópico: " + topic + ", Payload: " + payload.decode('utf-8'))
    else:
        print("Erro ao enviar dados. Código de retorno: " + str(result))

    # Espera por um intervalo de tempo
    time.sleep(5)
