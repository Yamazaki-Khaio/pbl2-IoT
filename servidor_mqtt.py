import paho.mqtt.client as mqtt
import json
import threading

from flask import Flask, jsonify

postos = []
broker_address = "localhost"
broker_port = 1883
broker_topic_carros = "dadoscarros"
broker_topic_postos = "dadospontos"

posto_menor_fila = None
client = mqtt.Client()
app = Flask(__name__)

def processar_dados_posto(payload):
    global postos, menor_fila_posto
    dados = json.loads(payload)
    posto_id = dados["id"]
    menor_fila = None
    for i, posto in enumerate(postos):
        if posto["id"] == posto_id:
            postos[i] = dados  # atualizar os dados do posto na lista
        if menor_fila is None or posto["fila"] < menor_fila["fila"]:
            menor_fila = posto
    if menor_fila is None or dados["fila"] < menor_fila["fila"]:
        menor_fila = dados
    postos.append(dados)  # adicionar novos dados do posto à lista
    menor_fila_posto = menor_fila  # atualizar o valor da menor fila do posto

def processar_dados_carro(payload):
    if isinstance(payload, bytes):
        payload = payload.decode('utf-8')
    dados = json.loads(payload)
    if dados["bateria"] < 20 and dados["descarga"] == "lenta":
        print("Enviar alerta para o motorista")
        # Aqui você pode adicionar o código para enviar uma mensagem MQTT ao motorista
    else:
        print("Dados do carro recebidos com sucesso")

        # Se a bateria estiver baixa, obter a localização do posto com menor fila
        if dados["bateria"] < 30:
            global posto_menor_fila
            if posto_menor_fila is not None:
                endereco_posto_menor_fila = posto_menor_fila["endereco"]
                print(f"O posto com menor fila é {posto_menor_fila['nome']}")
                dados["endereco_posto_menor_fila"] = endereco_posto_menor_fila
                # Publicar os dados atualizados do carro no broker MQTT
                client.publish(broker_topic_postos, payload.encode("utf-8"), qos=0)

            else:
                print("Não há postos disponíveis no momento")



def on_message(client, userdata, message):
    global postos, posto_menor_fila
    if message.topic == broker_topic_postos:
        payload_p = message.payload.decode("utf-8")
        processar_dados_posto(payload_p)

        print(f"Recebido o seguinte {payload_p} do tópico {message.topic}:")
    elif message.topic == broker_topic_carros:
        payload_c = message.payload.decode("utf-8")
        processar_dados_carro(payload_c)
        print(f"Recebido o seguinte {payload_c} do tópico {message.topic}:")

client.on_message = on_message
client.connect(broker_address, broker_port)
client.subscribe(broker_topic_carros, qos=0)
client.subscribe(broker_topic_postos, qos=0)

def start_mqtt_loop():
    client.loop_start()
mqtt_thread = threading.Thread(target=start_mqtt_loop)
mqtt_thread.start()



@app.route('/postos/menor-fila')
def get_posto_menor_fila():
    global menor_fila_posto
    if menor_fila_posto is None:
        return jsonify({"message": "Não há postos disponíveis no momento"})
    return jsonify(menor_fila_posto)

if __name__ == '__main__':
    app.run()