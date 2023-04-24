import json
import paho.mqtt.client as mqtt
from flask import Flask, jsonify

# Configurações do MQTT broker
broker_address = "localhost"
broker_port = 1883
broker_topic_posto = "dadospontos"

# Inicialização do cliente MQTT
client = mqtt.Client()
client.connect(broker_address, broker_port)

# Inicialização do servidor Flask
app = Flask(__name__)

# Rota GET para obter posto com a menor fila
@app.route('/postos/menorfila')
def obter_posto_menor_fila():
    # Obter os dados dos postos do broker MQTT
    client.subscribe(broker_topic_posto)
    client.loop_start()
    postos = []
    def on_message(client, userdata, message):
        postos.append(json.loads(message.payload.decode("utf-8")))
    client.on_message = on_message
    time.sleep(5)
    client.loop_stop()

    # Encontrar o posto com menor fila
    posto_menor_fila = None
    for posto in postos:
        if not posto_menor_fila or posto["ocupacao"] < posto_menor_fila["ocupacao"]:
            posto_menor_fila = posto

    return jsonify(posto_menor_fila)

# Rodar o servidor Flask
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
