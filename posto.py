import random
import time
import json
import uuid
import paho.mqtt.publish as publish
from flask import Flask, jsonify

# Configurações do broker MQTT
broker_address = "localhost"
broker_port = 1883
broker_topic_postos = "dadospontos"

# Informações do posto
posto = {"id": str(uuid.uuid1()), "bairro": "Centro", "nome": "Posto Centro", "fila": 0}

# Publicar dados do posto no tópico MQTT
def publicar_dados_posto(posto):
    publish.single(broker_topic_postos + '/' + posto["id"], payload=json.dumps(posto).encode("utf-8"), qos=0, retain=False,
                   hostname=broker_address, port=broker_port)

# Gerar dados aleatórios da fila do posto
def gerar_dados_posto(posto):
    posto["fila"] = random.randint(0, 10)

# Iniciar servidor Flask
app = Flask(__name__)

# Rota GET para obter posto com a menor fila
@app.route('/postos/menorfila')
def obter_posto_menor_fila():
    topicos = [broker_topic_postos + '/' + posto["id"] for posto in postos]
    mensagens = publish.multiple(topicos, payload='', qos=0, retain=False, hostname=broker_address, port=broker_port)
    posto_menor_fila = None
    for mensagem in mensagens:
        payload = json.loads(mensagem.payload.decode("utf-8"))
        if not posto_menor_fila or payload["fila"] < posto_menor_fila["fila"]:
            posto_menor_fila = payload
    return jsonify(posto_menor_fila)

# Loop principal
while True:
    gerar_dados_posto(posto)
    publicar_dados_posto(posto)
    time.sleep(5)

