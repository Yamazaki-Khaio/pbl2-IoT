from flask import Flask, jsonify
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)

# Define as configurações do MQTT
broker_address = "localhost"
client_id = "ponto_recarga"
topic_prefix = "carro/"
qos = 1

# Dicionário que armazena as informações dos pontos de recarga
pontos_recarga = {
    "ponto01": {"capacidade": 1.0, "ocupacao": 0.0},
    "ponto02": {"capacidade": 1.0, "ocupacao": 0.0},
    "ponto03": {"capacidade": 1.0, "ocupacao": 0.0}
}

# Função de callback para o evento de conexão ao broker MQTT
def on_connect(client, userdata, flags, rc):
    print("Conectado ao broker MQTT com sucesso. Código de retorno: " + str(rc))
    for ponto in pontos_recarga:
        # Se inscreve no tópico correspondente a cada ponto de recarga
        client.subscribe(topic_prefix + ponto)

# Função de callback para o evento de recebimento de mensagem
def on_message(client, userdata, msg):
    # Extrai o ID do carro e o ponto de recarga a partir do tópico
    carro_id, ponto_recarga_id = msg.topic[len(topic_prefix):].split('/')
    
    # Converte o payload JSON em dicionário Python
    payload_dict = json.loads(msg.payload.decode('utf-8'))

    # Atualiza a ocupação do ponto de recarga correspondente
    pontos_recarga[ponto_recarga_id]["ocupacao"] += payload_dict["descarga"]
    if pontos_recarga[ponto_recarga_id]["ocupacao"] > pontos_recarga[ponto_recarga_id]["capacidade"]:
        pontos_recarga[ponto_recarga_id]["ocupacao"] = pontos_recarga[ponto_recarga_id]["capacidade"]
    
    # Exibe as informações do ponto de recarga
    print("Ponto de recarga " + ponto_recarga_id + ":")
    print("- Capacidade: " + str(pontos_recarga[ponto_recarga_id]["capacidade"]))
    print("- Ocupação: " + str(pontos_recarga[ponto_recarga_id]["ocupacao"]))
    print("- Disponibilidade: " + str(pontos_recarga[ponto_recarga_id]["capacidade"] - pontos_recarga[ponto_recarga_id]["ocupacao"]))

# Configura o cliente MQTT
client = mqtt.Client(client_id)

# Configura as funções de callback
client.on_connect = on_connect
client.on_message = on_message

# Conecta ao broker MQTT
client.connect(broker_address)

# Rota que retorna o ponto de recarga com a menor fila
@app.route('/menor_fila')
def menor_fila():
    disponibilidades = [(ponto, pontos_recarga[ponto]["capacidade"] - pontos_recarga[ponto]["ocupacao"]) for ponto in pontos_recarga]
    menor_fila = sorted(disponibilidades, key=lambda x: x[1])[0]
    return jsonify({"ponto_recarga": menor_fila[0], "disponibilidade": menor_fila[1]})

if __name__ == '__main__':
    app.run()
